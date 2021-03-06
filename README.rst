###############
CongregationMS
###############

CongregationMS is a system (a Web Application) that can be used in the operations of one or more Congregations of the Jehovah's Witnesses.

This document is for developers who wants to know how to setup and run CongregationMS.

For more info about how to use the system, go to docs/_build/html/index.html.

============
Installation
============

-------------------------------
For local/development setting:
-------------------------------
    * Install python3. Optionally you can use virtual environment.
    * Install base packages, run ``pip install -r config/requirements/base.txt``.
    * Install local packages, run ``pip install -r config/requirements/local.txt``.
    * Make sure your environment variables are properly setup:

        - ``DJANGO_SETTINGS_MODULE=config.settings.local``
        - ``CONGREGATIONMS_SECRET_KEY=your_secret_key``

            + to create your own secret key, on another directory create an arbitrary django-project and you can use the generated secret key there. Run ``django-admin startproject``.

    * Run ``python manage.py migrate``
    * Run ``python manage.py createsuperuser`` and follow instructions.
    * Run ``python manage.py initial_data``. (Optional)

        - only run this management command in initial setup.
        - if you are already running a development environment, then there is no need to run this command.

    * You can start your development.
      

-------------------------------
For production setting:
-------------------------------
    * TODO


Management Commands for data setup:
    ``python manage.py initial_data``
    ``python manage.py cities_philippines``


Initial Setup:
```
python manage.py migrate
python manage.py initial_data
python manage.py cities_philippines
python manage.py createsuperuser
```
Create a Congregation
Create Groups within the Congregation
Create User(s)
    Give the user(s) the appropriate Authorization Group
Create Congregation Group(s) that the user is allowed to access