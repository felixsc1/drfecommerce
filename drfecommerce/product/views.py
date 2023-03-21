# from django.shortcuts import render
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

"""
See: https://www.django-rest-framework.org/api-guide/viewsets/
instead of defining what happens for get / post request etc. , we specify actions, such as "list"
also works together with router to automatically create endpoints.
"""


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=(CategorySerializer))
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing all products
    """

    queryset = Product.objects.is_active()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        queryset = self.queryset.filter(slug=slug)
        # select_related is just a tool to reduce the number of db queries
        serializer = ProductSerializer(
            queryset.select_related("category", "brand")
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")),
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(responses=(ProductSerializer))
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path=r"category/(?P<slug>[\w-]+)/all")
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug), many=True
        )
        return Response(serializer.data)
