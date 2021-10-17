"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from service.models import Product, DataValidationError, db

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
        init_db(app)

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

    # def _create_pets(self, count):
    #     """Factory method to create pets in bulk"""
    #     pets = []
    #     for _ in range(count):
    #         test_pet = PetFactory()
    #         resp = self.app.post(
    #             BASE_URL, json=test_pet.serialize(), content_type=CONTENT_TYPE_JSON
    #         )
    #         self.assertEqual(
    #             resp.status_code, status.HTTP_201_CREATED, "Could not create test pet"
    #         )
    #         new_pet = resp.get_json()
    #         test_pet.id = new_pet["id"]
    #         pets.append(test_pet)
    #     return pets

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)

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

    def test_delete_a_product(self):
        """Delete a product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    
