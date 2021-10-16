import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, PdtStatus

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n:n)
    name = factory.Faker("random_name")
    category = FuzzyChoice(choices = ['phone', 'table', 'computer', 'curtain'])
    amount = FuzzyChoice(choices = [1,2,3,4,5,6,7,8,9,10])
    status = FuzzyChoice(choices = [Status.Good, Status.Normal, Status.Bad, Status.Unknow])    