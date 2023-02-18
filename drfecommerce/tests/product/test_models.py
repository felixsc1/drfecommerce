import pytest

pytestmark = pytest.mark.django_db # otherwise get error that test has no access to db.


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