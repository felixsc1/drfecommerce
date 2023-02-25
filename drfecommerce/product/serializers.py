from rest_framework import serializers

from .models import Brand, Category, Product, ProductImage, ProductLine


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


class ProductLineSerializer(serializers.ModelSerializer):
    # the name "product_image" was specified in the ProductImage model under
    # foreign_key -> related_name
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
        )


class ProductSerializer(serializers.ModelSerializer):
    # goal: instead of convoluted output category / brand etc., with name keys inside,
    # we just want a property "category_name" in main content. (=Flattening)
    brand_name = serializers.CharField(source="brand.name")
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
        ]
