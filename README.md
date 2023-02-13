# Django Rest Framework - Ecommerce Tutorial Project

Based on udemy course.

## Changes to default setup

To follow best practices some things were done before creating an app:

- Default settings.py file is split up into local and production settings (in /settings folder) that import from base settings.
- django secret key was moved to .env file and imported.
- installed pytest-django and created pytest.ini file.
