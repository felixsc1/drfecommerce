from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from .fields import OrderField


class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


# Same thing done with custom manager (but overkill for such a simple task):
# class ActiveManager(models.Manager):
#     # this would override the model.objects.all() method:
#     # def get_queryset(self):
#     #     return super().get_queryset().filter(is_active=True)
#     # this adds a new option:  model.objects.isactive()
#     def isactive(self):
#         return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=False)

    # the manager runs when calling Product.objects.all() or Product.objects.isactive()
    # default manager would be models.Manager()
    # objects = ActiveManager()
    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)

    objects = ActiveQueryset.as_manager()

    # See https://docs.djangoproject.com/en/4.1/ref/models/instances/
    # clean is one step in model validation, where validation needs access to multiple fields.
    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        # Check for duplicate order values:
        for obj in qs:
            if self.id != obj.id and obj.order == self.order:
                raise ValidationError(
                    {"order": "ProductLine with this order already exists."}
                )
                # note: by using error with dict format and "order" key, it will show the error exactly
                # where it is in the admin interface.

    def __str__(self):
        return str(self.sku)
