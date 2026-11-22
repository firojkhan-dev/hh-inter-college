# H.H. Inter College Website

A Django-powered website for H.H. Inter College, Mohammadpur Babai, Chandausi, Sambhal, Uttar Pradesh.

## Features
- Public college homepage with college information, facilities and contact details.
- Dynamic teacher, notice and gallery content managed through Django Admin.
- Public contact and admission enquiry forms.
- Secure Django staff sign-in and a protected staff dashboard.
- Role gate based on Django's built-in staff/superuser permissions.
- CSRF-protected POST logout and Django session authentication.

## Technology
- Python
- Django
- MySQL
- HTML, CSS and JavaScript

## Project structure
~~~text
config/                  Django project settings and URL configuration
website/                 Public pages, models, forms, admin and staff portal
website/templates/       Django HTML templates
website/static/          CSS and JavaScript assets
media/                   Uploaded college images and notices
~~~

## Local setup
1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment.
3. Install the dependencies used by your deployment environment (Django 6.1.x and the MySQL driver).
4. Create a local .env file. Do not commit it.

Example environment variables:

~~~dotenv
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=3306
~~~

5. Create the MySQL database and grant the configured user access.
6. Run:

~~~bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Open http://127.0.0.1:8000/ for the public website, /staff/login/ for staff access, and /admin/ for Django Admin.

## Staff access
Only active Django users with Staff status enabled can use the staff portal. Create named accounts for each authorised staff member. Superusers can open Django Admin from the staff dashboard.

Read [AUTHENTICATION.md](AUTHENTICATION.md) for the login flow, access rules and production security checklist.

## Tests and checks
~~~bash
python manage.py test website
python manage.py check
python manage.py check --deploy
~~~

Run tests with the same database driver and environment configuration as the project. check --deploy should be run with production settings.

## Security notes
- Never commit .env, database credentials or DJANGO_SECRET_KEY.
- Use HTTPS in production and secure session/CSRF cookies.
- Keep DEBUG=False in production.
- Student-specific authentication is not yet part of this release; the staff portal is not a student login system.
