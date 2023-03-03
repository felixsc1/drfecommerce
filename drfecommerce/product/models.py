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
    # note: if related_name is same as model name, can be omitted, thats the default.
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product"
    )

    # the manager runs when calling Product.objects.all() or Product.objects.isactive()
    # default manager would be models.Manager()
    # objects = ActiveManager()
    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute}-{self.attribute_value}"


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )

    # determines what is returned when model.objects.all() is called:
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

    # enforce clean to be called whenever an instance is created, even from command line:
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductLineAttributeValue(models.Model):
    # A table that links a ProductLine to Attributes
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_attribute_value_pl"
    )

    class Meta:
        unique_together = ("product_line", "attribute_value")

    def clean(self):
        # Here, we want to check if duplicate attributes exist
        # qs returns true (false) if filter finds that new attribute_value
        # already exists for given product file
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value
            )
            .filter(product_line=self.product_line)
            .exists()
        )

        if not qs:
            # Here we traverse through two tables using the related_names
            # to get all attributes associated to a given product_line
            iqs = Attribute.objects.filter(
                attribute_value__product_line_attribute_value=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError(
                    {"attribute_value": "This attribute already exists."}
                )

    def save(self, *args, **kwargs):
        # again, just make sure clean gets initiated even when using command line.
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and obj.order == self.order:
                raise ValidationError(
                    {"order": "ProductImage with this order already exists."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order)


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attribute = models.ManyToManyField(
        Attribute,
        through="ProductTypeAttribute",
        related_name="product_type_attribute",
    )

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    # Link table between ProductType and Attribute
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute_pt"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="product_type_attribute_a"
    )

    class Meta:
        unique_together = ("product_type", "attribute")
        # unique together means, there should be no duplicates where product_type and attribute are both the same.
        # though individually they can appear multiple times.
