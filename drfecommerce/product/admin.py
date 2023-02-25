from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductImage, ProductLine


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


# @admin.register(Product)  # alternative way...
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine, ProductLineAdmin)
