import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db  # otherwise get error that test has no access to db.


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        data = category_factory(name="my_test_string_123")
        # Assert
        # test if __str__ method is working
        assert data.__str__() == "my_test_string_123"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        # Act
        data = brand_factory(name="my_test_string_123")
        # Assert
        # test if __str__ method is working
        assert data.__str__() == "my_test_string_123"


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        data = product_factory(name="test_product_123")
        # Assert
        # test if __str__ method is working
        assert data.__str__() == "test_product_123"


class TestProductLineModel:
    def test_str_methode(self, product_line_factory):
        data = product_line_factory(sku="test_product_line_123")
        assert data.__str__() == "test_product_line_123"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        # we also specify product_factory, 
        # since we want to create two product lines for the same product.
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            # create identical order number and pass it through our clean method
            # note that by default clean() 
            # is only executed when entering data through the form,
            # NOT when entering through the terminal as here
            # see lesson68 (min 12:30) for how to override model save 
            # function to enforce it.
            product_line_factory(order=1, product=product).clean()
