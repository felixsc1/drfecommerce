from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
)


class EditLinkInline(object):
    # see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#admin-reverse-urls
    # for how we got to this url.
    # an "instance" is one row in the product_line table.
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe(f'<a href="{url}">Edit</a>')
            return link
        else:
            return ""


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)  # access the edit function within EditLinkInline


class AttributeValueInline(admin.TabularInline):
    # for many-to-many relationship need to specify the related name
    model = AttributeValue.product_line_attribute_value.through


class AttributeValueProductInline(admin.TabularInline):
    # for many-to-many relationship need to specify the related name
    model = AttributeValue.product_attr_value.through


# @admin.register(Product)  # alternative way...
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline, AttributeValueProductInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Attribute)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(AttributeValue)
