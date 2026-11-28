# Website ko live kaise karein - beginner deployment guide

Yeh guide is project ko **Ubuntu 24.04 VPS + apna domain + MySQL + Nginx + Gunicorn + HTTPS** par chalane ka example deti hai. Aap kisi aur hosting provider par ja rahe hain to wahan ke panel/commands alag honge, lekin Django ki taiyaari ke steps milte-julte rahenge.

> **Abhi ka status:** Local project ke 24 tests pass hue hain. Iska matlab yeh nahi ki website internet par live ya production-ready prove ho gayi. Is workspace se aapka domain, hosting, production database, email provider, DNS aur HTTPS verify nahi kiye gaye.

## 1. Live karne ke liye abhi kya chahiye?

| Cheez | Abhi kya pata hai | Aapko kya karna hoga |
| --- | --- | --- |
| Hosting/server | Koi production server verify nahi hua | Ubuntu VPS ya Django-compatible managed hosting lena |
| Domain aur DNS | Actual live domain nahi mila | Domain lena aur DNS ko server ke public IP par point karna |
| Code bhejne ka tareeka | Workspace abhi Git repository nahi hai | Private Git remote banana, ya secure SFTP/SSH se files copy karna |
| Production web server | Local development `runserver` par based hai | Production mein Gunicorn aur Nginx/systemd (ya hosting ka equivalent) chalana |
| Production database | Code MySQL use karta hai; live DB verify nahi hai | Production MySQL database/user banana aur environment variables dena |
| HTTPS | Live TLS certificate verify nahi hua | Domain DNS set hone ke baad certificate lena aur HTTPS test karna |
| Static files | `STATIC_ROOT` configured hai | `collectstatic` chalana aur `/static/` ko Nginx/CDN se serve karna |
| Uploaded media | `MEDIA_ROOT` project ke `media/` folder mein hai; production URL serving configured nahi | Existing media copy/backup karna, persistent storage rakhna aur `/media/` serve karna |
| Email | SMTP account/credentials verify nahi | SMTP provider aur notification recipient set karke real email test karna |
| Operations | Production backups/monitoring verify nahi | Database + media backups, error logs aur renewal/update process rakhna |

`requirements-production.txt` mein Gunicorn rakha gaya hai, jo Linux par Django WSGI app ko serve karega. Nginx ke peeche HTTPS chalane ke liye settings mein optional trusted-proxy flag bhi hai.

## 2. Pehle yeh details taiyaar rakhein

Deploy shuru karne se pehle yeh values apne paas rakhein:

1. Domain, jaise `college.example.in`, aur kya `www.college.example.in` bhi use hoga.
2. VPS ka public IPv4 address (aur IPv6 tabhi jab aap use configure karenge).
3. Hosting/server par SSH access aur `sudo` permission.
4. Database ka naam, user aur strong password.
5. College notification ke liye office email aur SMTP provider ki details.
6. Agar purani site/database mein asli records hain to database aur `media/` folder ka backup.

Is guide mein `college.example.in` sirf example hai. **Har jagah apne asli domain se replace karein.** Kisi bhi secret/password ko chat, Git, screenshot ya public document mein share na karein.

## 3. VPS aur domain taiyaar karein

1. Ubuntu 24.04 VPS banayein. Chhoti site ke liye kam-se-kam 1-2 GB RAM se shuru kiya ja sakta hai; traffic aur uploads ke hisaab se badhayein.
2. Domain DNS mein:
   - Root domain (`@`) ka `A` record VPS IPv4 par point karein.
   - `www` ko `CNAME` se root domain par point karein, ya uska `A` record set karein.
   - `AAAA` record tabhi banayein jab server par IPv6 poori tarah set ho.
3. Hosting firewall aur server firewall mein SSH (22), HTTP (80) aur HTTPS (443) allow karein. Database port `3306` ko public internet par open na karein.
4. DNS update hone ke baad domain ko check karein. Certificate issue karne se pehle domain server tak resolve hona chahiye.

## 4. Server packages install karein

SSH se server par login karke:

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-venv python3-dev build-essential pkg-config default-libmysqlclient-dev mysql-server nginx
```

`mysqlclient` ko build karne ke liye Linux par development packages chahiye; upar wale packages Ubuntu example ke liye hain. Managed MySQL use karte hain to local `mysql-server` install karna zaroori nahi, lekin provider se database host, TLS aur access rules lein.

## 5. Production database banayein

Local MySQL example:

```bash
sudo mysql
```

MySQL prompt ke andar, placeholders ko apni values se badal kar:

```sql
CREATE DATABASE hh_inter_college CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hhweb'@'localhost' IDENTIFIED BY 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD';
GRANT ALL PRIVILEGES ON hh_inter_college.* TO 'hhweb'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Database ko public internet se accessible na banayein. Agar aapki current website/database mein content hai, pehle uska tested backup lein aur data import plan banayein; naya database banana purana data transfer nahi karta.

## 6. Project files server par rakhein

Is workspace mein Git repository/remote abhi set nahi hai. Isliye pehle VS Code se private Git repository bana kar code push karein, ya SSH/SFTP se files server par copy karein. `.env`, passwords, `.venv/` aur `venv/` ko upload/commit na karein. Existing `media/` files ko alag se copy karein agar database unke paths refer karta hai.

Dedicated service account aur app folder banayein:

```bash
sudo adduser --system --group --home /srv/hh-inter-college hhcollege
sudo -u hhcollege git clone YOUR_PRIVATE_REPOSITORY_URL /srv/hh-inter-college/app
```

Git use nahi kar rahe hain to `git clone` ki jagah project files ko `/srv/hh-inter-college/app/` mein copy karein, phir ownership check karein:

```bash
sudo chown -R hhcollege:hhcollege /srv/hh-inter-college
```

Virtual environment aur production packages install karein:

```bash
sudo -u hhcollege python3 -m venv /srv/hh-inter-college/app/.venv
sudo -u hhcollege /srv/hh-inter-college/app/.venv/bin/pip install --upgrade pip
sudo -u hhcollege /srv/hh-inter-college/app/.venv/bin/pip install -r /srv/hh-inter-college/app/requirements-production.txt
```

## 7. Secret environment file configure karein

Secret key generate karne ke liye server par chalayein:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Output ko private jagah rakhein. Systemd ke liye project folder ke bahar private file pehle secure permissions ke saath banayein, phir edit karein:

```bash
sudo install -o root -g root -m 600 /dev/null /etc/hh-inter-college.env
sudo nano /etc/hh-inter-college.env
```

Is file mein yeh values daalein; example domains/emails/credentials ko apni values se replace karein:

```dotenv
DJANGO_SECRET_KEY=PASTE_THE_GENERATED_SECRET_HERE
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=college.example.in,www.college.example.in
DJANGO_CSRF_TRUSTED_ORIGINS=https://college.example.in,https://www.college.example.in

DB_NAME=hh_inter_college
DB_USER=hhweb
DB_PASSWORD=REPLACE_WITH_THE_DATABASE_PASSWORD
DB_HOST=localhost
DB_PORT=3306

DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_TRUST_PROXY_SSL_HEADER=True

# HTTPS ko pehle poori tarah test karne tak HSTS band rakhein.
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False

DJANGO_EMAIL_HOST=smtp.your-provider.example
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_USER=website@your-domain.example
DJANGO_EMAIL_PASSWORD=REPLACE_WITH_SMTP_PASSWORD
DJANGO_EMAIL_USE_TLS=True
DJANGO_EMAIL_USE_SSL=False
DJANGO_DEFAULT_FROM_EMAIL=website@your-domain.example
COLLEGE_NOTIFICATION_EMAIL=office@your-domain.example
```

`DJANGO_TRUST_PROXY_SSL_HEADER=True` sirf is Nginx setup ke saath use karein jahan Gunicorn localhost par bound ho aur Nginx `X-Forwarded-Proto` header ko khud set/overwrite karta ho. Isse Django ko pata chalta hai ki visitor HTTPS par aaya hai aur SSL redirect loop nahi banta. Gunicorn ko public internet par directly expose na karein.

## 8. Database migration, admin aur static files

Pehle backup ka intezam karein. Agar database pehle se use ho raha hai, migration se pehle database aur media dono ka backup lein. App folder mein:

```bash
cd /srv/hh-inter-college/app
sudo -u hhcollege .venv/bin/python manage.py check
sudo -u hhcollege .venv/bin/python manage.py migrate
sudo -u hhcollege .venv/bin/python manage.py createsuperuser
sudo -u hhcollege .venv/bin/python manage.py collectstatic --noinput
```

- `migrate` website ke naye tables/fields banata hai; ise sahi production database credentials ke saath hi chalayein.
- `createsuperuser` aapka private Django Admin account banata hai. Password strong rakhein aur shared account na banayein.
- `collectstatic` static CSS/JS/Admin files ko `staticfiles/` mein jama karta hai.
- Project ka `media/` folder uploads ke liye hai. Use deploy ke dauraan delete/overwrite na karein; iska alag backup aur persistent storage hona chahiye.

## 9. Gunicorn ko systemd service ke roop mein chalayein

Service file kholein:

```bash
sudo nano /etc/systemd/system/hh-inter-college.service
```

Yeh content daalein:

```ini
[Unit]
Description=H.H. Inter College Django website
After=network.target mysql.service

[Service]
User=hhcollege
Group=hhcollege
WorkingDirectory=/srv/hh-inter-college/app
EnvironmentFile=/etc/hh-inter-college.env
ExecStart=/srv/hh-inter-college/app/.venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 config.wsgi:application
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

`After=network.target mysql.service` mein `mysql.service` sirf tab rakhein jab MySQL isi VPS par install hai. Managed database use karne par ise hata dein.

Service start aur status check karein:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hh-inter-college
sudo systemctl status hh-inter-college
sudo journalctl -u hh-inter-college -n 100 --no-pager
```

`active (running)` ka matlab process chalu hai; iska matlab abhi website public HTTPS par ready hai aisa nahi. Woh Nginx, DNS aur certificate ke baad test hoga.

## 10. Nginx configure karein

```bash
sudo nano /etc/nginx/sites-available/hh-inter-college
```

`college.example.in` ko apne domain se badal kar:

```nginx
server {
    listen 80;
    server_name college.example.in www.college.example.in;

    location /static/ {
        alias /srv/hh-inter-college/app/staticfiles/;
    }

    location /media/ {
        alias /srv/hh-inter-college/app/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Site enable aur Nginx syntax test karein:

```bash
sudo ln -s /etc/nginx/sites-available/hh-inter-college /etc/nginx/sites-enabled/hh-inter-college
sudo nginx -t
sudo systemctl reload nginx
```

Agar default Nginx page ya error aaye to DNS, `server_name`, file permissions aur Nginx logs check karein:

```bash
sudo journalctl -u nginx -n 100 --no-pager
```

## 11. HTTPS certificate lagayein

DNS sahi hone aur HTTP site khulne ke baad:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d college.example.in -d www.college.example.in
```

Certbot ke prompts follow karein aur HTTP se HTTPS redirect enable karein. Phir browser se dono URLs test karein:

- `https://college.example.in/`
- `https://www.college.example.in/`

HTTPS par homepage, `/admin/`, images, CSS aur forms check karein. SSL ke baad Nginx HTTPS request ke liye bhi `X-Forwarded-Proto: https` bhej raha hai yeh confirm karein.

## 12. Email aur HSTS test karein

### Email

SMTP provider ke diye hue host/port/user/password ko secret environment file mein set karke service restart karein:

```bash
sudo systemctl restart hh-inter-college
```

Website se test contact/admission submission bhejein. Confirm karein ki record database mein save hua aur notification sahi office inbox mein aayi. Spam folder aur provider ke SMTP logs bhi check karein. Agar email fail ho, enquiry phir bhi save ho sakti hai; server logs check karein:

```bash
sudo journalctl -u hh-inter-college -n 200 --no-pager
```

### HSTS

HTTPS sahi chalne ke baad hi HSTS par faisla karein. Shuruaat mein chhota period, jaise `DJANGO_SECURE_HSTS_SECONDS=3600`, rakhein aur test karein. Baad mein hi period badhayein. `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True` tabhi karein jab **har** subdomain HTTPS par ho. `DJANGO_SECURE_HSTS_PRELOAD=True` tabhi karein jab preload ki requirements samajh kar domain ko long-term HTTPS-only rakh sakte hon. Galat HSTS policy browsers mein lamba samay tak site access rok sakti hai.

HSTS chalu hone par `check --deploy` subdomain/preload settings ke baare mein warnings de sakta hai. Un warnings ko hatane ke liye settings ko bina soche `True` na karein; poora domain aur uske subdomains HTTPS par hone chahiye. Preload browser lists mein add hona alag, long-term decision hai.

Environment file badalne ke baad:

```bash
sudo systemctl restart hh-inter-college
```

## 13. Final production checks

Asli production environment variables load hone ke baad:

```bash
cd /srv/hh-inter-college/app
sudo -u hhcollege .venv/bin/python manage.py check --deploy
```

HSTS abhi jaan-boojhkar band hai to Django ka HSTS warning expected ho sakta hai. Baaki warnings ko samjhe bina ignore na karein. Is project mein current sample production-shaped check ne HSTS warning di thi; woh actual domain/hosting ka test nahi tha.

Browser se yeh checklist poori karein:

- Homepage desktop aur mobile par khulti hai.
- `/admin/` login page khulta hai; superuser login kaam karta hai.
- `/staff/login/` aur permission wala staff workflow test hota hai.
- HTTPS par CSS, JavaScript, logo, gallery, teacher photos aur notice attachments dikhte hain.
- Contact aur admission form valid/invalid input dono par sahi response dete hain.
- Email notification office inbox mein aati hai.
- HTTP se HTTPS redirect hota hai; `www` aur non-`www` ka chosen canonical behavior consistent hai.
- Server restart ke baad website wapas chalti hai.
- Database aur `media/` ka backup restore karne ka tareeka maloom hai.

## 14. Backup aur regular maintenance

- Database ka automatic, encrypted backup schedule karein; backup ko usi VPS par akela na chhodein.
- `media/` folder ka bhi backup lein. Database backup ke bina media references aur media backup ke bina image files dono adhoore hain.
- Backup restore ko test karein; backup file hona restore hone ka proof nahi.
- OS, Django aur dependencies ke security updates schedule karein. Update se pehle backup aur staging/test karein.
- Service errors `journalctl -u hh-inter-college` aur Nginx errors check karne ka process tay karein.
- SMTP password, DB password aur Django secret ko rotate karne ka tareeka rakhein.

## Launch se pehle yaad rakhein

`python manage.py runserver` development ke liye hai, public production server ke liye nahi. Real site tabhi launch samjhein jab asli domain, DNS, production database, HTTPS, static/media delivery, email aur backup/restore sab actual host par test ho chuke hon. Production database par migration se pehle backup lein. Hosting provider aur domain aap select karke values set karenge; is document ne koi service account, DNS record ya server create nahi kiya hai.
