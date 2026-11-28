# H.H. Inter College: URL, features aur dynamic website guide

Yeh document project ke maujooda Django code ko samjhata hai: `/staff/login/` route kaise kaam karta hai, feature files kahan rakhi hain, aur naye features ko kaise manage karna hai.

## 1. Abhi kya bana hai?

Website ke public aur staff routes ko alag modules mein rakha gaya hai. Homepage ke har major section ka apna template partial hai. College content, enquiry records aur staff workflows Django models/Admin se manage hote hain.

Is update mein ye 10 features shamil hain:

1. Searchable notice archive, notice detail pages, category aur expiry controls.
2. Admission enquiry status tracking: New, In Progress, Contacted, Admitted, Rejected.
3. Admin-managed homepage heading, address, phone, email, office hours, map aur social links.
4. Gallery albums, Hindi/English captions aur album filters.
5. Teacher profile pages, bilingual description aur display ordering.
6. Staff dashboard shortcuts, recent records aur permission-checked queues.
7. Admin-managed About, Academics aur Facilities information pages.
8. Website search: notices, teachers, information pages aur gallery.
9. Hindi/English public UI and content fields; missing Hindi text English fallback dikhata hai.
10. Optional staff email notifications for admission and contact forms.

## 2. Current URL map

`config/urls.py` Django Admin ko `/admin/` par mount karta hai aur website routes ko `website/urls.py` ke zariye include karta hai.

| Route | Naam | Access / use |
| --- | --- | --- |
| `/` | `home` | Public homepage, contact form |
| `/admission-enquiry/` | `admission_enquiry` | Public admission form |
| `/notices/` | `notice_list` | Published notices ka searchable/paginated archive |
| `/notices/<id>/` | `notice_detail` | Active, non-expired notice |
| `/gallery/` | `gallery_list` | Active gallery; `?album=<id>` se filter |
| `/teachers/<id>/` | `teacher_detail` | Active teacher profile |
| `/pages/<slug>/` | `information_page` | Admin se published information page |
| `/search/` | `site_search` | Public content search |
| `/language/` | `switch_language` | CSRF-protected POST se language preference |
| `/staff/login/` | `staff_login` | Authorised college staff login |
| `/staff/dashboard/` | `staff_dashboard` | Signed-in staff overview |
| `/staff/admissions/` | `staff_admissions` | Admission view permission required |
| `/staff/admissions/<id>/status/` | `update_admission_status` | Admission change permission; POST only |
| `/staff/messages/` | `staff_messages` | Contact-message view permission required |
| `/staff/logout/` | `staff_logout` | Staff, CSRF-protected POST only |
| `/admin/` | `admin:index` | Django Admin; Django staff permission required |

### `/staff/login/` ko kaise samjhein

`website/url_routes/staff.py` mein route `staff_login` view se juda hai:

```python
path("staff/login/", staff_login, name="staff_login")
```

- `staff/login/` browser ka path hai.
- `staff_login` Python view request aur authentication sambhalta hai.
- `name="staff_login"` stable route name hai.

Templates mein `{% url 'staff_login' %}` aur Python mein `reverse("staff_login")` use karna hard-coded URL se behtar hai. Route path badalne par named links aasaan se update hote hain.

Staff login Django session authentication use karta hai. Sirf active `is_staff=True` users sign in kar sakte hain; dashboard har request par staff status check karta hai. Admission/contact lists ke liye alag Django model permissions hain. Login ka `next` redirect validate hota hai aur logout POST-only hai.

## 3. Files ko feature ke hisaab se kaise baanta hai

```text
config/
    urls.py
    settings.py
website/
    urls.py                  # Public/staff URL modules ka aggregator
    url_routes/
        public.py
        staff.py
    views/
        public.py
        admissions.py
        notices.py
        gallery.py
        teachers.py
        pages.py
        search.py
        language.py
        staff.py
    models/
        content.py            # Teachers, notices, gallery, pages, settings
        enquiries.py          # Admission enquiries aur contact messages
    forms/
        admissions.py
        contact.py
        staff.py
    admin/
        content.py
        enquiries.py
    services/
        notifications.py
    templates/website/
        sections/             # Homepage ka har major section apni file
        notices/
        gallery/
        teachers/
        pages/
        search/
        staff/
    static/website/
        css/features.css
        css/style.css
        js/script.js
```

Is project mein ek hi Django app ke andar feature modules choose kiye gaye hain. Isse code alag rehta hai aur existing database records ko naye Django apps mein move karne ki zaroorat nahi padti. Har chhote helper ke liye nayi file banana zaroori nahi; related code ko ek feature module mein rakhein.

## 4. Content ko Admin se manage karna

- **Website settings:** Django Admin mein `Website settings` ka ek record bana kar homepage heading, address, phone, public email, office hours, map aur social URLs bharein. Blank phone/email visitor ko galat placeholder dene ke bajaay nahi dikhte.
- **Notices:** English/Hindi title aur description, category, attached file, active flag aur optional expiry date manage karein. Inactive ya expired notices public list/search se chhupe hote hain.
- **Admission enquiries:** Har form submission `New` status se shuru hoti hai. Staff permission wale users status aur internal notes update kar sakte hain.
- **Gallery:** Pehle album banayein, phir photos ko album se jodein. Inactive album ki images public listing se chhupi rehti hain.
- **Teachers:** Profile, photo, subject, qualification aur display order manage karein. Profile detail public tabhi hoti hai jab teacher active ho.
- **Information pages:** About, Academics aur Facilities ke bilingual default pages migration se bante hain. Admin mein content edit, unpublish ya naye slug wale pages add kar sakte hain.
- **Contact messages:** Staff message list dekh sakta hai; Admin mein `is_read` aur baaki fields manage kiye ja sakte hain.

Hindi text ke fields optional hain. Hindi field khaali ho to page English text use karta hai; publication se pehle Hindi translation ko staff se review karana chahiye.

## 5. Email notification setup

Local development mein email console par print hota hai. Production SMTP ke liye environment variables configure karein:

```dotenv
DJANGO_EMAIL_HOST=smtp.example.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_USER=website@example.com
DJANGO_EMAIL_PASSWORD=deployment-secret
DJANGO_EMAIL_USE_TLS=True
DJANGO_EMAIL_USE_SSL=False
DJANGO_DEFAULT_FROM_EMAIL=website@example.com
COLLEGE_NOTIFICATION_EMAIL=office@example.com
```

Values sirf deployment secret manager/environment mein rakhein; `.env` ya password ko Git mein commit na karein. SMTP/recipient set na ho ya mail provider fail ho to enquiry database mein save rehti hai aur server log mein notification failure aata hai. Production par SMTP ko configured karke test email zaroor bhejein.

## 6. Changes ko test karne ka tareeka

Local environment mein required Python packages, database variables aur MySQL service set hone ke baad:

```bash
python manage.py migrate
python manage.py test website
python manage.py check
python manage.py check --deploy
```

`check --deploy` production settings ke saath chalayein. Naye pages/routes ke tests mein URL reverse, public/permission access, Hindi fallback, inactive/expired content aur form submissions check karein.

## 7. Internet par live hone ki taiyaari

Code tests pass hona live deployment ka proof nahi hai. Is workspace se domain/DNS, hosting account, HTTPS certificate, production MySQL ya SMTP account verify nahi kiye gaye.

Deployment se pehle:

- `DJANGO_DEBUG=False`, unique secret key aur valid `DJANGO_ALLOWED_HOSTS` set karein.
- Production database credentials aur MySQL driver available hon.
- `DJANGO_CSRF_TRUSTED_ORIGINS` mein actual HTTPS origin configure karein.
- HTTPS, secure session/CSRF cookies aur SSL redirect verify karein.
- HTTPS ko verify karne ke baad `DJANGO_SECURE_HSTS_SECONDS` set karein; HSTS ko bina TLS/domain verify kiye enable na karein.
- `python manage.py migrate` aur `python manage.py collectstatic` chalayein.
- Media uploads ke liye persistent/suitable storage aur database/media backups configure karein.
- SMTP notification recipient/provider test karein.
- Production environment par `python manage.py check --deploy` ke warnings resolve karein.
- Deployed site par forms, staff permissions, static files aur mobile layout ko manually verify karein.

**Nateeja:** features aur code organization add kiye gaye hain, lekin internet par live hone ke liye tayyar hone ka final claim tabhi hoga jab hosting/domain/HTTPS/production database/SMTP configuration us environment mein verify ho.

Ubuntu VPS deployment ke detailed commands ke liye [LIVE_DEPLOYMENT_GUIDE_HI.md](LIVE_DEPLOYMENT_GUIDE_HI.md) dekhein.
