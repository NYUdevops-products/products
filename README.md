[![Build Status](https://app.travis-ci.com/NYUdevops-products/products.svg?branch=main)](https://app.travis-ci.com/NYUdevops-products/products)


# project-products

## Overview

This project is a class project for NYU Devops class.


## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own README.md file so be selective in what you copy.

There are two hidden files that you will need to copy manually if you use the Finder to copy files from this folder into your repo folder. They are:

```bash
    cp .coveragerc ../<your_repo_folder>/
    cp .gitignore  ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.devcontainers      - support for VSCode Remote Containers
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                - service python package
├── __init__.py         - package initializer
├── error_handlers.py   - HTTP error handling code
├── models.py           - module with business models
├── routes.py           - module with service routes
└── status.py           - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── factories.py    - factory for product
├── test_models.py  - test suite for busines models
└── test_routes.py  - test suite for service routes

Vagrantfile         - sample Vagrant file that installs Python 3 and PostgreSQL
```

## Service Descriptions
The following operations can be performed on the product services

```text
List all products: [GET] /products
List products by ID: [GET] /products/int:id
Create a new product: [POST] /products
Update a product: [PUT] /products/int:id
Delete a product: [DELETE] /products/int:id
Increase like count of a product: [PUT] /products/addlike/int:id
```

## How to run

```bash
Vagrant init ->
vagrant up ->
vargrant ssh ->
cd vagrant/ ->
FLASK_APP=service:app flask run -h 0.0.0.0
```
## How to test

```bash
Vagrant init ->
vagrant up ->
vargrant ssh ->
cd vagrant/ ->
Nosetests
```
This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.
