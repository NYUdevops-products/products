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
from service.models import db
from service.routes import app, init_db

DATABASE_URI=os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL="/products"
CONTENT_TYPE_JSON="application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

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
        resp = self.app.delete( "{0}/{1}".format(BASE_URL, test_pet.id), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        
        # to check and make sure the product is deleted
        resp = self.app.get("{0}/{1}".format(BASE_URL, test_product.id), content_type=CONTENT_TYPE_JSON )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
