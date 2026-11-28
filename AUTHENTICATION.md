# Staff Authentication

## Overview
The staff portal uses Django's built-in authentication and session framework. It does not add JWTs, third-party identity providers, or custom password storage.

## Routes

| Route | Purpose | Access |
| --- | --- | --- |
| /staff/login/ | Staff sign-in | Public entry point |
| /staff/dashboard/ | College record overview | Authenticated staff only |
| /staff/admissions/ | Review and filter admission enquiries | Staff with admission view permission |
| /staff/admissions/<id>/status/ | Update enquiry status and internal notes | Staff with admission change permission; POST only |
| /staff/messages/ | Review contact messages | Staff with contact-message view permission |
| /staff/logout/ | End staff session | Staff, POST only |
| /admin/ | Django administration | Active users with Django staff permission |

## Access rules
- A user must be active and have Django's is_staff=True flag to sign in.
- The dashboard checks is_staff on every request.
- Admission and contact queues enforce Django model permissions separately from is_staff; assign only the required view/change permissions to each staff account or group.
- A regular public/student account receives HTTP 403 if it attempts to access the dashboard.
- Superusers see the Admin Panel shortcut. Staff accounts without superuser status do not.
- Logout is POST-only and protected by Django CSRF middleware.
- The login view validates the next destination against the current host to prevent open redirects.

## Request flow
1. A staff member opens /staff/login/.
2. The browser submits username, password and a CSRF token over HTTPS in production.
3. Django's AuthenticationForm delegates credential checking to Django's configured authentication backend.
4. Django verifies the submitted password against the password hash stored for that user. The application never stores or logs the submitted password.
5. Only active staff accounts are logged in. Django creates/updates the session and sends the session identifier in its session cookie.
6. AuthenticationMiddleware resolves the session on later requests and exposes the authenticated account as request.user.
7. The dashboard enforces staff status. Admission and contact queues additionally check their Django model permissions before displaying records.
8. A CSRF-protected POST to /staff/logout/ ends the session.

The session cookie is not a JWT or a reusable API access token. Django's CSRF token is a separate request-forgery protection mechanism, not proof of identity.

## Create staff accounts
Create accounts through Django Admin or a trusted deployment shell. Set Staff status only for people authorised to use the portal. Do not create shared staff accounts.

Example shell commands:

~~~bash
python manage.py createsuperuser
python manage.py shell
~~~

For a staff account created in the shell:

~~~python
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_user(
    username="college-staff",
    password="use-a-unique-strong-password",
    is_staff=True,
)
~~~

Use a secure secret manager or deployment environment variables for production credentials. Never commit .env, database passwords, or DJANGO_SECRET_KEY to Git.

## Deployment checklist
- Set DJANGO_DEBUG=False.
- Configure DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS, and database environment variables.
- Serve the site over HTTPS and enable DJANGO_SESSION_COOKIE_SECURE=True and DJANGO_CSRF_COOKIE_SECURE=True.
- Configure SMTP and COLLEGE_NOTIFICATION_EMAIL before relying on staff submission notifications.
- Run migrations and python manage.py check --deploy in the deployment environment.
- Keep Django and dependencies patched.
- Create named accounts with least privilege; revoke access when staff leave.

## Current scope
This release adds staff/admin portal access and a protected staff overview. Student accounts, student-specific dashboards, self-service registration and email-based password reset are intentionally not enabled until a student identity/admission verification process and production email provider are configured.
