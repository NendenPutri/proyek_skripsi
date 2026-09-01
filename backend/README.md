# LaptopWise Backend

Backend LaptopWise adalah API FastAPI untuk rekomendasi laptop, autentikasi admin, CRUD laptop admin, penggabungan data CSV + MySQL, dan inferensi kategori laptop baru menggunakan pipeline Naive Bayes. Panduan full-stack ada di [../README.md](../README.md).

Backend tidak melakukan training ulang, scraping, upload dataset, upload model, import CSV dari dashboard, atau penulisan data admin ke CSV.

## Teknologi

- FastAPI
- SQLAlchemy
- Alembic
- PyMySQL
- Pandas
- NumPy
- Scikit-learn `1.6.1`
- Joblib
- bcrypt
- pytest

## Artefak Wajib

Pastikan file berikut tersedia:

```text
backend/data/laptops_backend_ready.csv
backend/data/frontend_options.json
backend/models/naive_bayes_laptop_pipeline.joblib
backend/models/model_metadata.json
```

## Menjalankan Backend Lokal

Dari folder `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Isi `backend/.env`, buat database MySQL, jalankan migration, lalu start backend:

```powershell
alembic upgrade head
python scripts\create_admin.py --name "Admin Utama" --email "admin@example.com" --password "password-kuat"
fastapi dev main.py
```

URL lokal:

- Backend: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`

## Contoh backend/.env Lokal

```env
APP_NAME=Sistem Rekomendasi Laptop API
APP_VERSION=1.0.0
API_PREFIX=/api
DATABASE_URL=mysql+pymysql://laptopwise_user:password_yang_benar@127.0.0.1:3306/laptopwise
JWT_SECRET_KEY=isi_secret_panjang_acak
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Contoh backend/.env Production VPS

```env
APP_NAME=Sistem Rekomendasi Laptop API
APP_VERSION=1.0.0
API_PREFIX=/api
DATABASE_URL=mysql+pymysql://laptopwise_user:password_database_vps@127.0.0.1:3306/laptopwise
JWT_SECRET_KEY=secret_panjang_acak_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Gunakan credential dan JWT secret milik server sendiri. Jangan commit `.env`.

## CORS Local dan Vercel

Backend membaca `BACKEND_CORS_ORIGINS` dari environment variable. Beberapa origin dipisahkan koma.

Local development:

```env
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Production VPS untuk frontend Vercel:

```env
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Restart backend setelah mengubah `.env`.

## Setup MySQL

Contoh untuk development lokal:

```sql
CREATE DATABASE IF NOT EXISTS laptopwise
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'laptopwise_user'@'localhost'
  IDENTIFIED BY 'password_yang_benar';

CREATE USER IF NOT EXISTS 'laptopwise_user'@'127.0.0.1'
  IDENTIFIED BY 'password_yang_benar';

GRANT ALL PRIVILEGES ON laptopwise.* TO 'laptopwise_user'@'localhost';
GRANT ALL PRIVILEGES ON laptopwise.* TO 'laptopwise_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

## Migration Alembic

Migration tersedia di:

```text
backend/alembic/versions/20260711_0001_create_admins_laptops.py
```

Migration membuat tabel:

- `admins`
- `laptops`

Jalankan dari folder `backend/`:

```powershell
alembic upgrade head
```

Cek revision aktif:

```powershell
alembic current
```

## Create Admin Pertama

Admin dibuat lewat script internal. Tidak ada register admin publik.

```powershell
python scripts\create_admin.py --name "Admin Utama" --email "admin@example.com" --password "password-kuat"
```

Alternatif lewat environment variable PowerShell:

```powershell
$env:ADMIN_NAME="Admin Utama"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="password-kuat"
python scripts\create_admin.py
```

Script menyimpan password sebagai hash dan tidak mencetak password ke log.

## Run Lokal Dengan FastAPI Dev

Command utama lokal:

```powershell
fastapi dev main.py
```

Jika terminal Windows mengalami error encoding dari CLI FastAPI, set:

```powershell
$env:PYTHONIOENCODING="utf-8"
fastapi dev main.py
```

## Production VPS Ringkas

Gambaran deployment:

1. Install Python, MySQL, Nginx, dan Certbot di VPS.
2. Salin folder `backend/` ke VPS.
3. Buat virtual environment dan install dependency.
4. Isi `backend/.env` production.
5. Pastikan artefak di `data/` dan `models/` lengkap.
6. Jalankan `alembic upgrade head`.
7. Buat admin pertama.
8. Jalankan backend sebagai service `systemd`.
9. Gunakan Nginx sebagai reverse proxy ke proses backend.
10. Aktifkan HTTPS dengan Certbot untuk `43-157-206-64.sslip.io`.

Contoh konsep Nginx:

```nginx
server {
    server_name 43-157-206-64.sslip.io;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Swagger production:

```text
https://43-157-206-64.sslip.io/docs
```

Health production:

```text
https://43-157-206-64.sslip.io/api/health
```

## Endpoint

Publik:

- `GET /`
- `GET /api/health`
- `GET /api/options`
- `GET /api/laptops`
- `POST /api/recommendations`
- `GET /api/model-info`

Admin:

- `POST /api/admin/auth/login`
- `GET /api/admin/auth/me`
- `GET /api/admin/dashboard/stats`
- `GET /api/admin/laptops`
- `GET /api/admin/laptops/{laptop_id}`
- `POST /api/admin/laptops`
- `PUT /api/admin/laptops/{laptop_id}`
- `DELETE /api/admin/laptops/{laptop_id}`

Semua endpoint admin selain login memakai:

```http
Authorization: Bearer TOKEN_ADMIN
```

## Test

```powershell
python -m pytest tests
```

## Troubleshooting Singkat

- `Access denied for user`: periksa `DATABASE_URL`, password, host MySQL, dan grant user.
- `JWT_SECRET_KEY wajib diisi`: isi `JWT_SECRET_KEY` di `.env`, lalu restart backend.
- CORS error: pastikan origin frontend masuk ke `BACKEND_CORS_ORIGINS`.
- Artefak tidak tersedia: pastikan file CSV, options JSON, Joblib, dan metadata JSON ada.
- `ModuleNotFoundError`: aktifkan `.venv`, lalu jalankan `python -m pip install -r requirements.txt`.
