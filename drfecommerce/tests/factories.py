import factory

from drfecommerce.product.models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # custom name can be passed by calling category_factory(name="some_string")
    # name = "test_category"
    # to have a unique name for each category:
    name = factory.Sequence(lambda n: f"test_category_{n}")
    slug = factory.Sequence(lambda n: f"test_category_{n}")


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"test_brand_{n}")


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = factory.Sequence(lambda n: f"test_attribute_{n}")
    description = factory.Sequence(lambda n: f"test_attribute_description_{n}")


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test_type"

    # see https://factoryboy.readthedocs.io/en/stable/reference.html?highlight=post_generation#factory.post_generation
    # for example use see: https://factoryboy.readthedocs.io/en/stable/recipes.html#simple-many-to-many-relationship
    # "attribute" is the many-to-many field inside ProductType.
    # if not empty, this function will add attributes (populate the link table).
    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"test_product_{n}")
    slug = factory.Sequence(lambda n: f"test_product_{n}")
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = factory.Sequence(lambda n: f"test_attribute_value_{n}")
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 10
    product = factory.SubFactory(ProductFactory)
    is_active = True

    # same as in AttributeType: many-to-many relationship
    # see test_models.py / TestProductLineModel for example how to call this.
    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test_alternative_text"
    url = "test.jpg"
    productline = factory.SubFactory(ProductLineFactory)
