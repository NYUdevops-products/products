"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from retry import retry
from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.adapters import Replay429Adapter
from requests import HTTPError, ConnectionError


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
# db = SQLAlchemy()

# def init_db(app):
#     """Initialies the SQLAlchemy app"""
#     Product.init_db(app)


# get configuration from environment (12-factor)
ADMIN_PARTY = os.environ.get('ADMIN_PARTY', 'False').lower() == 'true'
COUCHDB_HOST = os.environ.get('COUCHDB_HOST', 'localhost')
COUCHDB_USERNAME = os.environ.get('COUCHDB_USERNAME', 'admin')
COUCHDB_PASSWORD = os.environ.get('COUCHDB_PASSWORD', 'pass')

# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get('RETRY_COUNT', 10))
RETRY_DELAY = int(os.environ.get('RETRY_DELAY', 1))
RETRY_BACKOFF = int(os.environ.get('RETRY_BACKOFF', 2))


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class PdtStatus(Enum):
    # Enumeration of valid product states
    Good = 0
    Normal = 1
    Bad = 2
    Unknown = 4

class Product(db.Model):
    """
    Class that represents a <your resource model name>
    """
    # create a product(name="iPhone", category="phone", amount=1, description="the latest iPhone 13", status=PdtStatus.Good)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable = False)
    category = db.Column(db.String(63), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    status = db.Column(
        db.Enum(PdtStatus), nullable = False, server_default =(PdtStatus.Unknown.name) 
    )

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Pet into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "amount": self.amount,
            "status": self.status.name,  # convert enum to string
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            self.id = data["id"]
            self.name = data["name"]
            self.category = data["category"]
            self.amount = data["amount"]
            self.status = getattr(PdtStatus, data["status"])  # create enum from string
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a YourResourceModel by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category:str) -> list:
        """Returns all of the Pets in a category
        :param category: the category of the Pets you want to match
        :type category: str
        :return: a collection of Pets in that category
        :rtype: list
        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)


############################################################
#  C L O U D A N T   D A T A B A S E   C O N N E C T I O N
############################################################

    @staticmethod
    def init_db(dbname='pets'):
        """
        Initialized Coundant database connection
        """
        opts = {}
        vcap_services = {}
        # Try and get VCAP from the environment or a file if developing
        if 'VCAP_SERVICES' in os.environ:
            Product.logger.info('Running in Bluemix mode.')
            vcap_services = json.loads(os.environ['VCAP_SERVICES'])
        # if VCAP_SERVICES isn't found, maybe we are running on Kubernetes?
        elif 'BINDING_CLOUDANT' in os.environ:
            Product.logger.info('Found Kubernetes Bindings')
            creds = json.loads(os.environ['BINDING_CLOUDANT'])
            vcap_services = {"cloudantNoSQLDB": [{"credentials": creds}]}
        else:
            Product.logger.info('VCAP_SERVICES and BINDING_CLOUDANT undefined.')
            creds = {
                "username": COUCHDB_USERNAME,
                "password": COUCHDB_PASSWORD,
                "host": COUCHDB_HOST,
                "port": 5984,
                "url": "http://"+COUCHDB_HOST+":5984/"
            }
            vcap_services = {"cloudantNoSQLDB": [{"credentials": creds}]}

        # Look for Cloudant in VCAP_SERVICES
        for service in vcap_services:
            if service.startswith('cloudantNoSQLDB'):
                cloudant_service = vcap_services[service][0]
                opts['username'] = cloudant_service['credentials']['username']
                opts['password'] = cloudant_service['credentials']['password']
                opts['host'] = cloudant_service['credentials']['host']
                opts['port'] = cloudant_service['credentials']['port']
                opts['url'] = cloudant_service['credentials']['url']

        if any(k not in opts for k in ('host', 'username', 'password', 'port', 'url')):
            Product.logger.info('Error - Failed to retrieve options. ' \
                             'Check that app is bound to a Cloudant service.')
            exit(-1)

        Product.logger.info('Cloudant Endpoint: %s', opts['url'])
        try:
            if ADMIN_PARTY:
                Product.logger.info('Running in Admin Party Mode...')
            Productet.client = Cloudant(opts['username'],
                                  opts['password'],
                                  url=opts['url'],
                                  connect=True,
                                  auto_renew=True,
                                  admin_party=ADMIN_PARTY,
                                  adapter=Replay429Adapter(retries=10, initialBackoff=0.01)
                                 )
        except ConnectionError:
            raise AssertionError('Cloudant service could not be reached')

        # Create database if it doesn't exist
        try:
            Product.database = Product.client[dbname]
        except KeyError:
            # Create a database using an initialized client
            Product.database = Product.client.create_database(dbname)
        # check for success
        if not Product.database.exists():
            raise AssertionError('Database [{}] could not be obtained'.format(dbname))