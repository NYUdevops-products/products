import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product

class ProductFactory(factory.Factory):
    create a product(name="iPhone", category="phone", amount=1, description="the latest iPhone 13", status="Status.Good")
    