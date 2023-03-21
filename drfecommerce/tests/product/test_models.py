import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from drfecommerce.product.models import Category

pytestmark = pytest.mark.django_db  # otherwise get error that test has no access to db.


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        data = category_factory(name="my_test_string_123")
        # Assert
        # test if __str__ method is working
        assert data.__str__() == "my_test_string_123"

    def test_name_max_length(self, category_factory):
        name = "x" * 101
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            # run the validation check:
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 101
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="my_test_string_123")
        with pytest.raises(IntegrityError):
            category_factory(name="my_test_string_123")

    def test_parent_category_on_delete_protect(self, category_factory):
        obj1 = category_factory()
        category_factory(parent=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_category_active_only_true(self, category_factory):
        # tests our custom manager
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_category_active_only_false(self, category_factory):
        # Good idea to check if default behavior of manager,
        # upon which we extended, still works.
        category_factory(is_active=False)
        category_factory(is_active=True)
        qs = Category.objects.count()
        assert qs == 2


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        data = product_factory(name="test_product_123")
        # Assert
        # test if __str__ method is working
        assert data.__str__() == "test_product_123"

        # some more tests skipped here, are essentially the same as for Category


class TestProductLineModel:
    def test_duplicate_attribute_inserts(
        self,
        product_line_factory,
        attribute_factory,
        attribute_value_factory,
        product_line_attribute_value_factory
    ):
        obj1 = attribute_factory(name="shoe-color")
        obj2 = attribute_value_factory(attribute_value="red", attribute=obj1)
        obj3 = attribute_value_factory(attribute_value="blue", attribute=obj1)
        obj4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj2, product_line=obj4)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(
                attribute_value=obj3, product_line=obj4
            )
    
    def test_str_method(self, product_line_factory):
        # attr = attribute_value_factory(attribute_value="test_123")
        data = product_line_factory(sku="123")
        assert data.__str__() == "123"

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

    def test_field_decimal_places(self, product_line_factory):
        price = 0.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="12345")
        obj2 = product_image_factory(order=1, product_line=obj1)
        assert obj2.__str__() == "12345_img"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory):
        # test = attribute_factory(name="test_123")
        obj = product_type_factory.create(name="test_type")
        assert obj.__str__() == "test_type"


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute")
        obj_b = attribute_value_factory(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory.create(name="test_attribute")
        assert obj.__str__() == "test_attribute"
