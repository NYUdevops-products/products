"""
My Service

Describe what your service does here
"""

from enum import Enum
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import PdtStatus, Product, DataValidationError, DatabaseConnectionError

# Import Flask application
from . import app

# Document the type of autorization required
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'X-Api-Key'
#     }
# }

######################################################################
# GET INDEX
######################################################################
# @app.route("/")
# def index():
#     """Root URL response"""
#     app.logger.info("Request for Root URL")
#     return (
#         jsonify(
#             name="Product Demo REST API Service",
#             version="1.0",
#             paths=url_for("list_products", _external=True),
#         ),
#         status.HTTP_200_OK,
#     )


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    # data = '{name: <string>, category: <string>}'
    # url = request.base_url + 'products' # url_for('list_products')
    # return jsonify(name='product Demo REST API Service', version='1.0', url=url, data=data), status.HTTP_200_OK
    return app.send_static_file("index.html")


######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Product Demo REST API Service',
          description='This is a sample server Product server.',
          default='products',
          default_label='Product shop operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
        #   authorizations=authorizations,
          prefix='/api'
         )

# Define the model so that the docs reflect what can be sent
create_model = api.model('Product', {
    'name': fields.String(required=True,
                          description='The name of the Product'),
    'category': fields.String(required=True,
                              description='The category of the Product (e.g.table, phone, etc.)'),
    'amount': fields.Integer(required=True,
                                description='The amount of the Products in stock'),
    'status': fields.String(enum=PdtStatus._member_names_, description='The status of the Product'),
    'likecount': fields.Integer(required=True,
                                description = 'The number of like count of the Product')
})


product_model = api.inherit(
    'ProductModel', 
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=False, help='List Products by name')
product_args.add_argument('category', type=str, required=False, help='List Products by category')
# product_args.add_argument('amount', type=int, required=False, help='List Products by availability')
# product_args.add_argument('status', type=PdtStatus, required=False, help='List Products by availability')
# product_args.add_argument('likecount', type=int, required=False, help='List Products by availability')

######################################################################
# Special Error Handlers
######################################################################

    # """ Root URL response """
    # return (
    #     "Reminder: return some useful information in json format about the service here",
    #     status.HTTP_200_OK,
    # )

######################################################################
#  PATH: /products/{id}
######################################################################
@api.route('/products/<int:products_id>')
@api.param('products_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /product{id} - Returns a product with the id
    PUT /product{id} - Update a product with the id
    DELETE /product{id} -  Deletes a product with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    #------------------------------------------------------------------
    @api.doc('get_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def get(self, products_id):
        """
        Retrieve a single product

        This endpoint will return a product based on it's id
        """
        app.logger.info("Request to Retrieve a product with id [%s]", products_id)
        product = Product.find(products_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(products_id))
        return product.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING PRODUCT
    #------------------------------------------------------------------
    @api.doc('update_products')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model)
    # @token_required
    def put(self, products_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info('Request to Update a Product with id [%s]', products_id)
        product = Product.find(products_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(products_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = products_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A PRODUCT
    #------------------------------------------------------------------
    @api.doc('delete_products')
    @api.response(204, 'Product deleted')
    # @token_required
    def delete(self, products_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info('Request to Delete a Product with id [%s]', products_id)
        product = Product.find(products_id)
        if product:
            product.delete()
            app.logger.info('Product with id [%s] was deleted', products_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products
######################################################################
@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):
    """ Handles all interactions with collections of Products """
    #------------------------------------------------------------------
    # LIST ALL products
    #------------------------------------------------------------------
    @api.doc('list_products')
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """ Returns all of the Products """
        app.logger.info('Request to list Products...')
        products = []
        args = product_args.parse_args()
        
        
        if args['category']:
            app.logger.info('Filtering by category: %s', args['category'])
            products = Product.find_by_category(args['category'])
        elif args['name']:
            app.logger.info('Filtering by name: %s', args['name'])
            products = Product.find_by_name(args['name'])
        else:
            app.logger.info('Returning unfiltered list.')
            products = Product.all()

        results = [product.serialize() for product in products]
        app.logger.info('[%s] Products returned', len(results))
        return results, status.HTTP_200_OK


    #------------------------------------------------------------------
    # ADD A NEW PRODUCT
    #------------------------------------------------------------------
    @api.doc('create_products')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    # @token_required
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info('Request to Create a Product')
        check_content_type("application/json")
        product = Product()
        app.logger.debug('Payload = %s', api.payload)
        product.deserialize(api.payload)
        product.create()
        app.logger.info('Product with new id [%s] created!', product.id)
        location_url = api.url_for(ProductResource, products_id=product.id, _external=True)
        return product.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    # ------------------------------------------------------------------
    # DELETE ALL PRODUCTS (for testing only)
    # ------------------------------------------------------------------
    # @api.doc('delete_all_products')
    # @api.response(204, 'All Products deleted')
    # # @token_required
    # def delete(self):
    #     """
    #     Delete all Product

    #     This endpoint will delete all Product only if the system is under test
    #     """
    #     app.logger.info('Request to Delete all products...')
    #     if "TESTING" in app.config and app.config["TESTING"]:
    #         Product.remove_all()
    #         app.logger.info("Removed all Products from the database")
    #     else:
    #         app.logger.warning("Request to clear database while system not under test")

    #     return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products/{id}/like
######################################################################
@api.route('/products/<product_id>/like')
@api.param('product_id', 'The Product identifier')
class LikeResource(Resource):
    """ Like actions on a Product """
    @api.doc('like_a_product')
    @api.response(404, 'Product not found')
    # @api.response(409, 'The Product is not available for purchase')
    def put(self, product_id):
        """
        Like a Product

        This endpoint will like a Product and add the 'likecount' by 1
        """
        app.logger.info('Request to Like a Product')
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, 'Product with id [{}] was not found.'.format(product_id))

        product.likecount = product.likecount + 1
        product.update()
        app.logger.info('Product with id [%s] has been liked!', product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

# def abort(error_code: int, message: str):
#     """Logs errors before aborting"""
#     app.logger.error(message)
#     api.abort(error_code, message)

# @app.before_first_request
# def init_db(dbname="products"):
#     """ Initlaize the model """
#     Product.init_db(dbname)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )