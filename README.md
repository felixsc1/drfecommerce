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

- Creating custom fields: 