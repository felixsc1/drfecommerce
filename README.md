# Django Rest Framework - Ecommerce Tutorial Project

Based on [udemy course](https://www.udemy.com/course/django-drf-project-ecommerce).

## Changes to default setup

To follow best practices some things were done before creating an app:

- Default settings.py file is split up into local and production settings (in /settings folder) that import from base settings.
- django secret key was moved to .env file and imported.

## Additional packages used

- [django-mptt](https://django-mptt.readthedocs.io/en/latest/index.html). Makes it easier to work with hierarchical data. Here, each product can have a category, which in turn may have sub-categories.
- [drf-spectacular](https://pypi.org/project/drf-spectacular/) to automatically create schema and swagger UI view.

## Testing

- installed pytest-django and created pytest.ini file.
- Optional packages: _converage_ or _pytest-cov_ can give some hints about missing tests (see lesson 48, they give the same information either in command line or as html report).
- [_pytest-factoryboy_](https://pypi.org/project/pytest-factoryboy/): Allows populating models for tests, so that code doesn't have to be repeated for each test.


## Notes

A few things I learned through this project:

About [ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/#viewset)
- The regular ViewSet class does not provide any actions. To add one, one has to override functions such as list, create, retrieve..
- ModelViewSet can be useful as it provides all get/post/update endpoints out of the box.
- Some features like get_queryset (used for filtering) is not available in ModelViewSet -> use GenericViewSet.

- Creating custom managers / querysets, that can e.g. filter out data based on some field (lesson 65).

- Creating custom fields: In field.py created order field that automatically increments an integer for ever newly added product line.

- Modify admin interface: Created inline to directly add product lines under a given products. Product Images are also an inline under product lines, which can be edited via a custom edit link button.

- Optimizing performance by reducing SQL queries: 
  - If a model contains foreign-keys and we filter this model, django performs an additional query to get data from each foreign-key table. Solution: `serializer = ProductSerializer(queryset.select_related("category", "brand"), many=True)` `select_related` behind the scenes creates a Join of all those tables, then filters (here, 1 query instead of 3)
  - Select_related does not work for reverse foreign keys (e.g. filtering a product, which contains many lines / images, the foreignkey field is in the image model, not in the product line model). Solution: [prefetch_selected](https://docs.djangoproject.com/en/4.1/ref/models/querysets/) `prefetch_related(Prefetch("product_line__product_image")`
  - Lesson 64 explains the packages needed to analyze the actual SQL queries that run behind the scenes.

- Creating many-to-many relationships with custom [link/through-table](https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django). Section 10 of course (but quite confusing)

- Re-structuring the output using to_representation() in serializers.


### Random Django notes

- Typically when referencing modelA as foreign key in modelB, modelB has to be placed below A in the code. This can be circumvented by using string "modelA" instead of the object modelA (without quotes).

## References
[very good article about serializers](https://testdriven.io/blog/drf-serializers/)