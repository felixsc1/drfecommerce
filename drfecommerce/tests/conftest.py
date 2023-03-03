import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    AttributeFactory,
    AttributeValueFactory,
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
    ProductTypeFactory,
)

# registering as camel case, but will then be available as "category_factory"
register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductTypeFactory)


@pytest.fixture
def api_client():
    return APIClient
