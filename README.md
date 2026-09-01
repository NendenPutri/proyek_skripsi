# LaptopWise

LaptopWise adalah sistem rekomendasi laptop berbasis web. Aplikasi membantu pengguna memilih laptop berdasarkan kebutuhan, budget, dan spesifikasi, lalu backend memberikan rekomendasi dari dataset laptop awal dan data laptop aktif yang ditambahkan admin.

README ini menjadi panduan utama untuk client atau pengembang lain agar bisa menjalankan project secara lokal dan memahami deployment production.

## Gambaran Sistem

LaptopWise terdiri dari:

- Frontend ReactJS + Vite untuk area publik dan area admin.
- Backend FastAPI sebagai API utama.
- MySQL untuk akun admin dan data laptop manual dari admin.
- Dataset CSV hasil preprocessing sebagai katalog laptop awal.
- Pipeline Naive Bayes Joblib untuk inferensi kategori laptop baru.
- `frontend_options.json` untuk pilihan form/filter.
- `model_metadata.json` untuk informasi model yang aman ditampilkan.

Frontend tidak menjalankan machine learning, tidak membaca CSV, dan tidak membaca file Joblib. Semua data runtime berasal dari backend API.

## Mode Penggunaan

### Local Development

Mode lokal menggunakan:

- Frontend: `http://localhost:5173`
- Backend: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`

Environment utama:

```env
# frontend/.env
VITE_API_BASE_URL=http://127.0.0.1:8000

# backend/.env
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Production Deployment

Mode production menggunakan:

- Frontend Vercel: `https://rekomendasi-laptop-alpha.vercel.app`
- Backend VPS: `https://43-157-206-64.sslip.io`
- Swagger: `https://43-157-206-64.sslip.io/docs`
- Health: `https://43-157-206-64.sslip.io/api/health`

Environment utama:

```env
# Vercel Environment Variable
VITE_API_BASE_URL=https://43-157-206-64.sslip.io

# backend/.env di VPS
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Perpindahan frontend dari backend lokal ke backend VPS cukup dilakukan dengan mengubah `VITE_API_BASE_URL`. Tidak perlu mengubah kode.

## URL Production

| Layanan | URL |
| --- | --- |
| Frontend | `https://rekomendasi-laptop-alpha.vercel.app` |
| Backend | `https://43-157-206-64.sslip.io` |
| Swagger | `https://43-157-206-64.sslip.io/docs` |
| Health | `https://43-157-206-64.sslip.io/api/health` |

## Catatan Deployment Final

URL production:

- Frontend: `https://rekomendasi-laptop-alpha.vercel.app`
- Backend: `https://43-157-206-64.sslip.io`
- Swagger: `https://43-157-206-64.sslip.io/docs`
- Health: `https://43-157-206-64.sslip.io/api/health`

Contoh path backend di VPS:

```text
/var/www/laptopwise/app/backend
```

Contoh env backend production:

```env
DATABASE_URL=mysql+pymysql://laptopwise_user:DB_PASSWORD@127.0.0.1:3306/laptopwise
JWT_SECRET_KEY=SECRET_PANJANG
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Env frontend Vercel:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

Restart backend:

```bash
sudo systemctl restart laptopwise-backend
```

Cek backend:

```bash
curl -s https://43-157-206-64.sslip.io/api/health
```

Cek Swagger:

```text
https://43-157-206-64.sslip.io/docs
```

Jika frontend masih request ke localhost:

- Cek Vercel Environment Variables.
- Pastikan `VITE_API_BASE_URL=https://43-157-206-64.sslip.io`.
- Redeploy frontend.
- Cek request di browser DevTools tab Network.

Jika CORS error:

- Cek `BACKEND_CORS_ORIGINS` di VPS.
- Pastikan origin frontend `https://rekomendasi-laptop-alpha.vercel.app` sudah masuk.
- Restart backend.

Jika login admin gagal:

- Pastikan admin sudah dibuat dengan `backend/scripts/create_admin.py`.
- Pastikan endpoint login memakai `/api/admin/auth/login`.
- Pastikan request admin setelah login mengirim `Authorization: Bearer TOKEN_ADMIN`.

Jangan menulis password database asli atau JWT secret asli di source code, README, atau dokumentasi publik.

## Struktur Project

```text
App/
|-- README.md
|-- backend/
|   |-- AGENTS.md
|   |-- README.md
|   |-- .env.example
|   |-- alembic.ini
|   |-- main.py
|   |-- requirements.txt
|   |-- alembic/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- db/
|   |   |-- repositories/
|   |   |-- schemas/
|   |   |-- services/
|   |   +-- utils/
|   |-- data/
|   |-- models/
|   |-- scripts/
|   +-- tests/
+-- frontend/
    |-- AGENTS.md
    |-- README.md
    |-- .env.example
    |-- index.html
    |-- package.json
    |-- vite.config.js
    |-- vercel.json
    +-- src/
        |-- assets/
        |-- components/
        |-- config/
        |-- contexts/
        |-- hooks/
        |-- pages/
        |-- services/
        |-- styles/
        +-- utils/
```

## Prasyarat

Install lebih dulu:

- Python 3.10 atau lebih baru.
- Node.js dan npm.
- MySQL Server.
- Git.
- Browser modern seperti Chrome, Edge, atau Firefox.

Cek versi:

```powershell
python --version
node -v
npm -v
mysql --version
git --version
```

## Artefak Runtime Backend

File berikut wajib tersedia:

```text
backend/data/laptops_backend_ready.csv
backend/data/frontend_options.json
backend/models/naive_bayes_laptop_pipeline.joblib
backend/models/model_metadata.json
```

Fungsi file:

- `laptops_backend_ready.csv`: katalog laptop awal dan kandidat rekomendasi dari hasil preprocessing.
- `frontend_options.json`: pilihan dropdown/filter untuk frontend publik dan admin.
- `naive_bayes_laptop_pipeline.joblib`: pipeline model Naive Bayes untuk inferensi.
- `model_metadata.json`: metadata model, fitur model, kelas, dan metrik yang aman ditampilkan.

Backend tidak menulis data admin ke CSV. Data laptop dari admin disimpan ke MySQL.

## Setup Backend Lokal

Masuk ke folder backend:

```powershell
cd backend
```

Buat dan aktifkan virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependency:

```powershell
python -m pip install -r requirements.txt
```

Salin env:

```powershell
Copy-Item .env.example .env
```

Isi `backend/.env` untuk lokal:

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

Jangan gunakan password atau JWT secret contoh untuk production.

### Setup MySQL Lokal

Masuk ke MySQL:

```powershell
mysql -u root -p
```

Buat database dan user:

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

Jalankan migration:

```powershell
alembic upgrade head
```

Cek migration:

```powershell
alembic current
```

Buat admin pertama:

```powershell
python scripts\create_admin.py --name "Admin Utama" --email "admin@example.com" --password "password-kuat"
```

Jalankan backend:

```powershell
fastapi dev main.py
```

Backend lokal berjalan di:

```text
http://127.0.0.1:8000
```

## Setup Frontend Lokal

Masuk ke folder frontend:

```powershell
cd frontend
```

Install dependency:

```powershell
npm install
```

Jika PowerShell memblokir npm:

```powershell
npm.cmd install
```

Salin env:

```powershell
Copy-Item .env.example .env
```

Isi `frontend/.env` untuk memakai backend lokal:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Jalankan frontend:

```powershell
npm run dev
```

Jika PowerShell memblokir npm:

```powershell
npm.cmd run dev
```

Frontend lokal berjalan di:

```text
http://localhost:5173
```

## Environment Frontend

Frontend membaca base URL backend dari `VITE_API_BASE_URL`.

Lokal:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Production Vercel:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

Catatan:

- Jangan isi `VITE_API_BASE_URL` dengan tambahan `/api`.
- Benar: `https://43-157-206-64.sslip.io`
- Endpoint service sudah menambahkan path seperti `/api/laptops`.
- Setelah mengubah env lokal, restart Vite.
- Setelah mengubah env di Vercel, redeploy frontend.

## Environment Backend

Backend membaca konfigurasi dari `backend/.env`.

Variable penting:

- `DATABASE_URL`: koneksi SQLAlchemy ke MySQL melalui PyMySQL.
- `JWT_SECRET_KEY`: secret untuk menandatangani token admin. Wajib diisi dan harus panjang/acak.
- `BACKEND_CORS_ORIGINS`: daftar origin frontend yang diizinkan, dipisahkan koma.

Contoh lokal:

```env
DATABASE_URL=mysql+pymysql://laptopwise_user:password_yang_benar@127.0.0.1:3306/laptopwise
JWT_SECRET_KEY=isi_secret_panjang_acak
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Contoh production VPS:

```env
DATABASE_URL=mysql+pymysql://laptopwise_user:password_database_vps@127.0.0.1:3306/laptopwise
JWT_SECRET_KEY=secret_panjang_acak_production
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Jangan commit `backend/.env`.

## Deployment VPS Ringkas

Backend production tersedia di:

```text
https://43-157-206-64.sslip.io
```

Gambaran deployment VPS:

1. Install Python, MySQL, Nginx, dan Certbot.
2. Salin folder `backend/` ke VPS.
3. Buat virtual environment dan install `requirements.txt`.
4. Isi `backend/.env` production.
5. Pastikan artefak runtime tersedia di `backend/data/` dan `backend/models/`.
6. Jalankan `alembic upgrade head`.
7. Buat admin pertama dengan `scripts/create_admin.py`.
8. Jalankan backend sebagai service `systemd`, misalnya memakai Uvicorn/FastAPI app.
9. Pasang Nginx sebagai reverse proxy dari domain `43-157-206-64.sslip.io` ke proses backend lokal VPS.
10. Pasang HTTPS menggunakan Certbot untuk domain `43-157-206-64.sslip.io`.

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

Setelah mengubah `backend/.env` di VPS, restart service backend.

## Deployment Vercel

Frontend production tersedia di:

```text
https://rekomendasi-laptop-alpha.vercel.app
```

Konfigurasi Vercel:

- Root project: `frontend/`.
- Build command: `npm run build`.
- Output directory: `dist`.
- Environment variable:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

File `frontend/vercel.json` menyediakan SPA rewrite agar refresh route seperti `/about` atau `/admin/laptops` tidak menjadi 404.

Setelah mengubah `VITE_API_BASE_URL` di Vercel, lakukan redeploy.

## Endpoint API Utama

Endpoint publik:

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| GET | `/` | Root backend |
| GET | `/api/health` | Status backend, database, dan artefak |
| GET | `/api/options` | Options untuk form dan filter |
| GET | `/api/laptops` | Daftar laptop publik |
| POST | `/api/recommendations` | Rekomendasi laptop |
| GET | `/api/model-info` | Informasi model |

Endpoint admin:

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| POST | `/api/admin/auth/login` | Login admin |
| GET | `/api/admin/auth/me` | Validasi sesi admin |
| GET | `/api/admin/dashboard/stats` | Statistik dashboard admin |
| GET | `/api/admin/laptops` | List laptop admin |
| GET | `/api/admin/laptops/{laptop_id}` | Detail laptop admin |
| POST | `/api/admin/laptops` | Tambah laptop admin |
| PUT | `/api/admin/laptops/{laptop_id}` | Edit laptop admin |
| DELETE | `/api/admin/laptops/{laptop_id}` | Nonaktifkan laptop admin |

Semua endpoint admin selain login wajib memakai header:

```http
Authorization: Bearer TOKEN_ADMIN
```

## Admin

Admin dibuat melalui script internal, bukan register publik.

Buat admin pertama:

```powershell
cd backend
.\.venv\Scripts\activate
python scripts\create_admin.py --name "Admin Utama" --email "admin@example.com" --password "password-kuat"
```

Login admin:

```http
POST /api/admin/auth/login
```

Payload:

```json
{
  "email": "admin@example.com",
  "password": "password-kuat"
}
```

Contoh response:

```json
{
  "success": true,
  "message": "Login admin berhasil.",
  "data": {
    "access_token": "TOKEN_ADMIN",
    "token_type": "bearer",
    "expires_in": 3600,
    "admin": {
      "id": 1,
      "name": "Admin Utama",
      "email": "admin@example.com",
      "is_active": true
    }
  }
}
```

Gunakan token untuk endpoint admin:

```http
Authorization: Bearer TOKEN_ADMIN
```

Password admin disimpan sebagai hash. Password asli tidak dapat dilihat ulang dari database.

## Testing

Backend:

```powershell
cd backend
.\.venv\Scripts\activate
python -m pytest tests
```

Frontend build:

```powershell
cd frontend
npm run build
```

Jika PowerShell memblokir npm:

```powershell
npm.cmd run build
```

## Troubleshooting

### CORS Error

Pastikan origin frontend masuk ke `BACKEND_CORS_ORIGINS`.

Lokal:

```env
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Production:

```env
BACKEND_CORS_ORIGINS=https://rekomendasi-laptop-alpha.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Restart backend setelah mengubah env.

### Frontend Masih Request ke Localhost

Periksa `frontend/.env` atau environment variable Vercel.

Lokal:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Production:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

Restart Vite atau redeploy Vercel setelah mengubah env.

### 401 Admin

Kemungkinan penyebab:

- Token belum dikirim.
- Token salah atau kedaluwarsa.
- `JWT_SECRET_KEY` berubah setelah token dibuat.
- Admin nonaktif.

Solusi:

- Login ulang admin.
- Pastikan header memakai `Authorization: Bearer TOKEN_ADMIN`.
- Pastikan `JWT_SECRET_KEY` production tetap konsisten.

### Backend Tidak Membaca Artefak Model

Pastikan file berikut tersedia:

```text
backend/data/laptops_backend_ready.csv
backend/data/frontend_options.json
backend/models/naive_bayes_laptop_pipeline.joblib
backend/models/model_metadata.json
```

Jalankan backend dari folder `backend/`:

```powershell
fastapi dev main.py
```

### MySQL Access Denied

Gejala:

```text
Access denied for user 'laptopwise_user'@'localhost'
```

Solusi:

- Periksa `DATABASE_URL`.
- Pastikan password benar.
- Pastikan user MySQL dibuat untuk host `localhost` dan/atau `127.0.0.1`.
- Jalankan ulang `GRANT ALL PRIVILEGES`.

### ModuleNotFoundError Backend

Aktifkan virtual environment dan install dependency:

```powershell
cd backend
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Catatan Keamanan

- Jangan commit `.env`.
- Jangan commit password database.
- Jangan commit password admin.
- Jangan commit JWT secret.
- Jangan menulis secret asli di README, source code, atau dokumentasi publik.
- Jangan menampilkan token di URL.
- Jangan membagikan token admin.
- Gunakan password admin yang kuat.
- Gunakan JWT secret yang panjang dan acak.
- Batasi CORS production ke domain frontend yang benar.
- Backup database sebelum operasi berisiko.

## Batasan Sistem

Sistem ini tidak menyediakan:

- Training ulang dari web.
- Upload model.
- Upload CSV.
- Upload dataset.
- Import CSV dari dashboard.
- Scraping.
- Payment.
- Transaksi pembelian.
- Register pengguna umum.
- Register admin publik.
- Forgot/reset password.

Sistem hanya melakukan inferensi menggunakan pipeline Naive Bayes yang sudah dilatih. Data admin disimpan ke MySQL dan tidak ditulis ulang ke CSV.

## File Penting Untuk Diserahkan

Pastikan paket project berisi:

- `README.md`
- `backend/`
- `frontend/`
- `backend/.env.example`
- `frontend/.env.example`
- `backend/data/laptops_backend_ready.csv`
- `backend/data/frontend_options.json`
- `backend/models/naive_bayes_laptop_pipeline.joblib`
- `backend/models/model_metadata.json`
