"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import PdtStatus, Product, DataValidationError, db
from service import app
from .factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  P R O D U C T S   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

  

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """Create a product and assert that it exists"""
        product = Product(name="apple", category="fruit", amount = 1, status=PdtStatus.Good)
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "apple")
        self.assertEqual(product.category, "fruit")
        self.assertEqual(product.amount, 1)
        self.assertEqual(product.status, PdtStatus.Good)
        product = Product(name="iphone", category="phone", amount = 0, status=PdtStatus.Normal)
        self.assertEqual(product.name, "iphone")
        self.assertEqual(product.amount, 0)
        self.assertEqual(product.status, PdtStatus.Normal)


    def test_find_product(self):
        """Find a Product by ID"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        logging.debug(product)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 3)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.amount, products[1].amount)
        self.assertEqual(product.category, products[1].category)
        self.assertEqual(product.status, products[1].status)
        self.assertEqual(product.likecount, products[1].likecount)


    def test_delete_a_product(self):
        """Delete a product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_update_a_product(self):
        """Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertEqual(product.id, 1)
        # Change it an save it
        product.category = "hotdog"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.category, "hotdog")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].category, "hotdog")

    def test_update_with_empty_id(self):
        """Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertEqual(product.id, 1)    
        product.category = "hotdog"
        # Change id an save it
        product.id = None
        # product.update()
        self.assertRaises(DataValidationError, product.update())        


    def test_serialize_a_product(self):
        """Test serialization of a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("amount", data)
        self.assertEqual(data["amount"], product.amount)
        self.assertIn("status", data)
        self.assertEqual(data["status"], product.status.name)
        self.assertIn("likecount", data)
        self.assertEqual(data["likecount"], product.likecount)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Product with missing data"""
        data = {"id": 1, "name": "iphone", "category": "phone"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)


    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_status(self):
        """ Test deserialization of bad status attribute """
        test_product = ProductFactory()
        data = test_product.serialize()
        data["status"] = "good" # wrong case
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.amount, products[1].amount)
        self.assertEqual(product.likecount, products[1].likecount)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)

    def test_find_by_name(self):
        """Find a Product by Name"""
        Product(name="iphone", category="phone", amount=1).create()
        Product(name="iphone13", category="phone", amount=2).create()
        products = Product.find_by_name("iphone")
        self.assertEqual(products[0].category, "phone")
        self.assertEqual(products[0].name, "iphone")
        self.assertEqual(products[0].amount, 1)