"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Product, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)


@app.route('/products', methods=['GET'])
def list_products():
    results = []
    category = request.args.get('category')
    if category:
        app.logger.info('Getting Products for category: {}'.format(category))
        results = Product.find_by_category(category)
    else:
        app.logger.info('Getting all Pets')
        results = Product.all()
    return jsonify([product.serialize() for product in results]), status.HTTP_200_OK