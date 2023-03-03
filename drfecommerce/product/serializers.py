from rest_framework import serializers

from .models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
)


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id", "productline"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ["attribute", "attribute_value"]


class ProductLineSerializer(serializers.ModelSerializer):
    # the name "product_image" was specified in the ProductImage model under
    # foreign_key -> related_name
    product_image = ProductImageSerializer(many=True)
    # if we didnt have the attributeserializer and just had the attributevalue in fields,
    # it would just show the foreign-key, but now we get an object with name and value
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        )

    def to_representation(self, instance):
        # See https://testdriven.io/blog/drf-serializers/ for explanation of the function
        # See Lesson 86 beginning, for before/after view of what we want to do here.
        representation = super().to_representation(instance)
        # pop() affects the original dictionary, not just a copy
        attr_value_data = representation.pop("attribute_value")
        attr_values_dict = {}
        for key in attr_value_data:
            attr_values_dict.update({key["attribute"]["id"]: key["attribute_value"]})
        # note: if same attribute_id is used twice, it will be overridden by update.
        # we added a validation check to prevent that.
        representation.update({"specification": attr_values_dict})
        return representation


class ProductSerializer(serializers.ModelSerializer):
    # goal: instead of convoluted output category / brand etc., with name keys inside,
    # we just want a property "category_name" in main content. (=Flattening)
    brand_name = serializers.CharField(source="brand.name")
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
            "attribute",
        ]

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        # Best to first run query on swagger with this function
        # commented/uncommented, to see effect.
        representation = super().to_representation(instance)
        type_spec_data = representation.pop("attribute")
        type_spec_dict = {}
        for key in type_spec_data:
            type_spec_dict.update({key["id"]: key["name"]})
        representation.update({"type specification": type_spec_dict})
        return representation
