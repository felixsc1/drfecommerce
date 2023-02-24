from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

"""
Goal of the orderfield: Automatically add an increasing integer
to every new product-line of a given product.
Will tell the front-end in which order to display items.

In models.py, this is used as:
order = OrderField(unique_for_field="product", blank=True)
unique_for_field tells it to perform a query for each product separately.
blank=True since we dont want to add it manually (otherwise would get error).

Watch lesson 66 for explanation of the code below.
"""


class OrderField(models.PositiveIntegerField):
    # see https://docs.djangoproject.com/en/4.1/howto/custom-model-fields/
    description = (
        "An integer that is automatically incremented each time a new product is added."
    )

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("OrderField must define a 'unique_for_field' attribute.")
            ]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [
                checks.Error(
                    "OrderField entered does not match an existing model field."
                )
            ]
        return []

    def pre_save(self, model_instance, add):
        """
        Every time new product line is created, the model fields pass through this function.

        First check if no value is provided (which we want, since it should add values automatically).
        It will then filter the product lines for the current product. (add print(qs) to see it)
        """
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            try:
                # the values below are for example:
                # self.unique_for_field = product
                # getattr(...) =  p1
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(**query)
                # self.attname is for example "order" since we use order = OrderField() in product lines
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            # if value is provided in admin field, just return it
            return super().pre_save(model_instance, add)
