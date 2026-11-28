# H.H. Inter College Website

A Django-powered website for H.H. Inter College, Mohammadpur Babai, Chandausi, Sambhal, Uttar Pradesh.

## Features
- Public college homepage with college information, facilities and contact details.
- Dynamic teacher, notice and gallery content managed through Django Admin.
- Public contact and admission enquiry forms.
- Secure Django staff sign-in and a protected staff dashboard.
- Role gate based on Django's built-in staff/superuser permissions.
- CSRF-protected POST logout and Django session authentication.
- Searchable notice archive with notice detail pages and expiry controls.
- Admission enquiry status tracking and permission-checked staff queues.
- Dynamic bilingual homepage settings, college information pages and gallery albums.
- Teacher profile pages and Hindi/English public content.
- Optional staff email notifications for admission and contact submissions.

## Technology
- Python
- Django
- MySQL
- HTML, CSS and JavaScript

## Project structure
~~~text
config/                  Django project settings and URL configuration
website/                 Website features split into models/forms/views/admin modules
website/templates/       Django HTML templates
website/static/          CSS and JavaScript assets
media/                   Uploaded college images and notices
~~~

## Local setup
1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment.
3. Install the project dependencies:

~~~bash
pip install -r requirements.txt
~~~

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
6. For production, configure `DJANGO_DEBUG=False`, valid `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, HTTPS/secure-cookie settings and `DJANGO_SECURE_HSTS_SECONDS` after HTTPS is confirmed. For email notifications, set SMTP variables (`DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_USER`, `DJANGO_EMAIL_PASSWORD`, `DJANGO_EMAIL_USE_TLS`) and `COLLEGE_NOTIFICATION_EMAIL` in the deployment environment. Do not commit credentials.
7. Run:

~~~bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Open http://127.0.0.1:8000/ for the public website, /staff/login/ for staff access, and /admin/ for Django Admin.

## Staff access
Only active Django users with Staff status enabled can use the staff portal. Create named accounts for each authorised staff member. Superusers can open Django Admin from the staff dashboard.

Read [AUTHENTICATION.md](AUTHENTICATION.md) for the login flow, access rules and production security checklist.

Read [URLS_DYNAMICITY_GUIDE.md](URLS_DYNAMICITY_GUIDE.md) for the current URL map, modularization options and ideas for expanding dynamic features.

Read [LIVE_DEPLOYMENT_GUIDE_HI.md](LIVE_DEPLOYMENT_GUIDE_HI.md) for a step-by-step Ubuntu VPS, MySQL, Nginx and HTTPS deployment guide in Hindi.

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
