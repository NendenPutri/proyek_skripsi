# LaptopWise Frontend

Frontend LaptopWise adalah aplikasi ReactJS + Vite + Tailwind CSS v4 untuk area publik dan area admin. Panduan full-stack ada di [../README.md](../README.md).

Frontend hanya mengumpulkan input pengguna/admin, memanggil backend API, dan menampilkan hasil. Frontend tidak membaca CSV, Joblib, atau MySQL secara langsung.

## Teknologi

- React `19`
- Vite `8`
- Tailwind CSS v4
- `@tailwindcss/vite`
- React Router DOM `7`
- Lucide React
- AOS
- ESLint

## Menjalankan Frontend Lokal

Dari folder `frontend/`:

```powershell
npm install
Copy-Item .env.example .env
npm run dev
```

Jika PowerShell memblokir npm:

```powershell
npm.cmd install
npm.cmd run dev
```

URL lokal default:

```text
http://localhost:5173
```

## Environment Frontend

Frontend membaca alamat backend dari `VITE_API_BASE_URL`.

Lokal:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Vercel production:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

Catatan:

- Jangan tambahkan `/api` di `VITE_API_BASE_URL`.
- Benar: `https://43-157-206-64.sslip.io`
- Endpoint service sudah menulis path seperti `/api/health` dan `/api/laptops`.
- Setelah mengubah `.env` lokal, restart Vite.
- Setelah mengubah env di Vercel, redeploy frontend.

## Integrasi Backend API

Semua request frontend harus melalui backend API dan service layer di `src/services/`.

Frontend tidak boleh:

- membaca CSV langsung;
- membaca file Joblib langsung;
- membaca MySQL langsung;
- menjalankan machine learning;
- membuat data dummy sebagai sumber runtime utama.

Service API utama:

- `src/services/apiClient.js`: client terpusat untuk base URL, header, token, parsing JSON, dan error.
- `src/config/api.js`: normalisasi `VITE_API_BASE_URL` dan endpoint.
- `src/services/healthService.js`
- `src/services/optionsService.js`
- `src/services/laptopService.js`
- `src/services/recommendationService.js`
- `src/services/modelInfoService.js`
- `src/services/adminAuthService.js`
- `src/services/adminLaptopService.js`
- `src/services/adminDashboardService.js`

Endpoint publik:

- `GET /api/health`
- `GET /api/options`
- `GET /api/laptops`
- `POST /api/recommendations`
- `GET /api/model-info`

Endpoint admin:

- `POST /api/admin/auth/login`
- `GET /api/admin/auth/me`
- `GET /api/admin/dashboard/stats`
- `GET /api/admin/laptops`
- `GET /api/admin/laptops/{laptop_id}`
- `POST /api/admin/laptops`
- `PUT /api/admin/laptops/{laptop_id}`
- `DELETE /api/admin/laptops/{laptop_id}`

Endpoint admin selain login memakai:

```http
Authorization: Bearer TOKEN_ADMIN
```

Token dikelola terpusat dan tidak boleh dicetak ke console.

## Cek Request di Browser DevTools

Untuk memastikan frontend memakai backend yang benar:

1. Buka aplikasi di browser.
2. Tekan `F12` atau `Ctrl+Shift+I`.
3. Buka tab `Network`.
4. Jalankan fitur seperti health, rekomendasi, login admin, atau list laptop.
5. Klik request API.
6. Pastikan Request URL sesuai mode yang digunakan.

Local development:

```text
http://127.0.0.1:8000/api/health
```

Production Vercel:

```text
https://43-157-206-64.sslip.io/api/health
```

Jika terlihat request ke `http://127.0.0.1:8000` saat aplikasi Vercel dibuka, berarti `VITE_API_BASE_URL` di Vercel belum diset atau belum redeploy.

## Route

Publik:

- `/`
- `/recommendation`
- `/laptops`
- `/about`
- `*`

Admin:

- `/admin/login`
- `/admin`
- `/admin/laptops`
- `/admin/laptops/create`
- `/admin/laptops/:id`
- `/admin/laptops/:id/edit`

Route admin selain login dilindungi protected route.

## Build

Build production:

```powershell
npm run build
```

Jika PowerShell memblokir npm:

```powershell
npm.cmd run build
```

Output build:

```text
frontend/dist/
```

Preview lokal:

```powershell
npm run preview
```

## Deployment Vercel

File `vercel.json` sudah tersedia untuk SPA rewrite agar refresh route seperti `/about` atau `/admin/laptops` tidak menjadi 404.

Konfigurasi Vercel:

- Root project: `frontend/`.
- Build command: `npm run build`.
- Output directory: `dist`.
- Environment variable:

```env
VITE_API_BASE_URL=https://43-157-206-64.sslip.io
```

Pastikan backend production mengizinkan domain frontend di `BACKEND_CORS_ORIGINS`.

## Troubleshooting Singkat

- Frontend masih request ke localhost di Vercel: set `VITE_API_BASE_URL` di Vercel lalu redeploy.
- CORS error: pastikan backend VPS memasukkan `https://rekomendasi-laptop-alpha.vercel.app` di `BACKEND_CORS_ORIGINS`.
- 401 admin: login ulang dan pastikan token dikirim sebagai `Authorization: Bearer TOKEN_ADMIN`.
- Backend tidak aktif: cek `GET /api/health`.
- Build gagal: jalankan `npm install`, lalu ulangi `npm run build`.
