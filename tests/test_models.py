"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from service.models import Product, DataValidationError, db
<<<<<<< HEAD
from service import app
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
=======

>>>>>>> e6be1a687846bc300da918f83bec04f1dd56746b
######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
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
        """Create a pet and assert that it exists"""
        product = Product(name="apple", category="fruit", available=True)
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "apple")
        self.assertEqual(product.category, "fruit")
        self.assertEqual(product.available, True)
        product = Product(name="pineapple", category="fruit", available=False)
        self.assertEqual(product.name, "pineapple")
        self.assertEqual(product.available, False)


    def test_find_product(self):
        """Find a Product by ID"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        logging.debug(product)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 3)
        # find the 2nd pet in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.amount, products[1].amount)
        self.assertEqual(product.category, products[1].category)
        self.assertEqual(product.description, products[1].description)
        self.assertEqual(product.status, products[1].status)

<<<<<<< HEAD
        def test_delete_a_product(self):
            """Delete a product"""
            product = ProductFactory()
            product.create()
            self.assertEqual(len(Product.all()), 1)
            # delete the product and make sure it isn't in the database
            product.delete()
            self.assertEqual(len(Product.all()), 0)
=======
    def test_delete_a_product(self):
        """Delete a product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)
>>>>>>> e6be1a687846bc300da918f83bec04f1dd56746b

    
 