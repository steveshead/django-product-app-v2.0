# Django - Product Display App v2.0

### This app displays a list of products with their images and descriptions, uploaded using a form. Version 2 has a product cart, with the usual cart functionality.

* Only registered users can upload products.
* Registered users will have the option to edit or delete products through the product detail page.
* When creating a product you have the option to upload an image, add an image url or leave both blank.
* Visitors can click on the product owners name to see all products by that owner.

##### The Product Display App is built using the following methods:

* Django template filters
* Django Forms and Model Forms
* Image Fields and image uploads
* User Authentication
* Django and AJAX to create a like button

##### The Product Display App uses the following packages:

* dj-database-url
* Django
* django-registration-redux
* django-widget-tweaks
* olefile
* Pillow
* python-decouple
* django-carton


All pages where a user name is used will first look for first name and last name.  If those don't exist it will default to username.

In the profile page, a users tagline will appear under the page heading.

You will need to create a .env file and add your secret key and database settings to it.  Take a look at the env.example file for examples of formatting.  Here's an idea of a basic .evn file:

```
SECRET_KEY = 'randomsetofnumberslettersandcharactersetc'
DEBUG=True
ALLOWED_HOSTS=.localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

To Install first create an virtual environment in the root directory.

```django
python3 -m venv myvenv
```
Activate the virtual environment

```django
source myvenv/bin/activate
```

Change directory to the project folder

```django
cd myproject
```

Install all dependencies

```django
pip install -r requirements.txt
```

Migrate schema

```django
python manage.py migrate
```

Create a superuser

```django
python manage.py createsuperuser
```

To Do:
* Create a base version so it can be themed
* Rebuild success page after form fill
* Add 'checkout' functionality to the cart
