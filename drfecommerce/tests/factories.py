import factory

from drfecommerce.product.models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductLineAttributeValue,
    ProductType,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # custom name can be passed by calling category_factory(name="some_string")
    # name = "test_category"
    # to have a unique name for each category:
    name = factory.Sequence(lambda n: f"test_category_{n}")
    slug = factory.Sequence(lambda n: f"test_slug_{n}")


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = factory.Sequence(lambda n: f"test_attribute_{n}")
    description = factory.Sequence(lambda n: f"test_attribute_description_{n}")


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: f"test_type_name_{n}")

    #     # see https://factoryboy.readthedocs.io/en/stable/reference.html?highlight=post_generation#factory.post_generation
    #     # for example use see: https://factoryboy.readthedocs.io/en/stable/recipes.html#simple-many-to-many-relationship
    #     # "attribute" is the many-to-many field inside ProductType.
    #     # if not empty, this function will add attributes (populate the link table).
    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"test_product_{n}")
    pid = factory.Sequence(lambda n: f"0000_{n}")
    description = "test_description"
    is_digital = True
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


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
    weight = 100
    product_type = factory.SubFactory(ProductTypeFactory)

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
    product_line = factory.SubFactory(ProductLineFactory)


class ProductLineAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLineAttributeValue

    product_line = factory.SubFactory(ProductLineFactory)
    attribute_value = factory.SubFactory(AttributeValueFactory)
