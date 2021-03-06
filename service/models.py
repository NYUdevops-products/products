"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialies the SQLAlchemy app"""
    Product.init_db(app)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""

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
    status = db.Column(db.Enum(PdtStatus), nullable = False, server_default =(PdtStatus.Unknown.name))
    likecount = db.Column(db.Integer, nullable = False, default = 0)
    
    
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
            "likecount": self.likecount,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            # self.id = data["id"]
            self.name = data["name"]
            self.category = data["category"]
            self.amount = data["amount"]
            self.status = getattr(PdtStatus, data["status"])  # create enum from string
            self.likecount = data["likecount"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            )

        # if there is no id and the data has one, assign it
        if not self.id and "_id" in data:
            self.id = data["_id"]

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
        """ Returns all of the Products in the database """
        logger.info("Processing all Products")
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
    def find_by_name(cls, name:str) -> list:
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