"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db, init_db
from service.routes import app
from .factories import ProductFactory

DATABASE_URI=os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL="/products"
CONTENT_TYPE_JSON="application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(TestCase):
    """ REST API Server Tests """

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
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            print("1111",test_product)
            resp = self.app.post(
                BASE_URL, json=test_product.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products
    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_product_list(self):
        resp = self.app.get('/products')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        
    def test_delete_product(self):
        """delete a product"""
        test_product = self._create_products(1)[0]
        resp = self.app.delete( "{0}/{1}".format(BASE_URL, test_product.id), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        
        # to check and make sure the product is deleted
        resp = self.app.get("{0}/{1}".format(BASE_URL, test_product.id), content_type=CONTENT_TYPE_JSON )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, json=test_product.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["category"] = "hotdog"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["category"], "hotdog")