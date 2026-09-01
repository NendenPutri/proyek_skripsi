# Frontend Agent Instructions

## Scope Kerja

- Seluruh pekerjaan agent wajib terbatas pada folder `frontend/`.
- Jangan membuat, mengubah, memindahkan, atau menghapus file di folder `backend/`.
- Jangan membuat, mengubah, memindahkan, atau menghapus file di luar folder `frontend/`.
- Baca struktur, pola komponen, service, hook, styling, routing, dan dokumentasi frontend yang sudah ada sebelum melakukan perubahan.
- Pertahankan fitur publik lama yang sudah berjalan.
- Jangan menghapus atau mengganti fitur publik lama hanya karena area admin ditambahkan.
- Jangan menambahkan fitur di luar kebutuhan frontend sistem rekomendasi laptop dan area admin yang ditentukan.
- Instruksi ini adalah panduan kerja agent frontend. Jangan mulai implementasi fitur kecuali pengguna secara eksplisit meminta implementasi.

## Konteks Aplikasi

- Frontend adalah aplikasi ReactJS yang dibangun dengan Vite.
- Styling menggunakan Tailwind CSS v4.
- Backend menggunakan FastAPI dan menjadi sumber utama seluruh data aplikasi.
- Frontend memiliki dua area utama:
  - area publik untuk pengguna umum;
  - area admin untuk pengelolaan data laptop.
- Area publik tetap menyediakan landing page, form rekomendasi, daftar laptop publik, informasi model, dan status backend.
- Area admin menyediakan login admin, validasi sesi admin, protected route, admin layout, dashboard sederhana, dan pengelolaan data laptop.
- Frontend hanya mengumpulkan input pengguna/admin, mengambil data API, mengirim request ke backend, dan menampilkan hasil.
- Frontend tidak menjalankan machine learning.
- Frontend tidak membaca file Joblib.
- Frontend tidak membaca dataset CSV secara langsung.
- Frontend tidak melakukan training, retraining, fitting, atau preprocessing dataset mentah.
- Frontend tidak membuat data dummy sebagai sumber data runtime.

## Area Publik yang Harus Tetap Berjalan

Pertahankan halaman dan behavior publik berikut:

- Beranda;
- halaman rekomendasi;
- form rekomendasi;
- hasil rekomendasi utama;
- hasil rekomendasi alternatif;
- halaman data laptop publik;
- halaman tentang sistem;
- halaman not found;
- status koneksi backend;
- loading state;
- error state;
- empty state;
- responsive layout.

Endpoint publik lama harus tetap digunakan melalui service layer:

- `GET /api/health`
- `GET /api/options`
- `GET /api/laptops`
- `POST /api/recommendations`
- `GET /api/model-info`

## Area Admin yang Termasuk Scope Frontend

Scope frontend baru mencakup:

- login admin;
- validasi sesi admin;
- penyimpanan access token secara terpusat;
- protected route;
- admin layout;
- dashboard admin sederhana;
- daftar data laptop admin;
- search;
- filter;
- sorting jika backend mendukung;
- pagination;
- detail laptop;
- tambah laptop manual;
- edit laptop;
- hapus atau nonaktifkan laptop;
- dialog konfirmasi;
- loading state;
- error state;
- empty state;
- notifikasi;
- menampilkan `predicted_category` dari backend;
- menampilkan `prediction_confidence` hanya jika backend mengirimkannya;
- responsive admin interface.

## Batasan Fitur

Jangan membuat:

- login pengguna umum;
- register pengguna umum;
- register admin publik;
- lupa password;
- reset password;
- dashboard pengguna umum;
- import CSV;
- upload CSV;
- upload dataset;
- upload model;
- training model;
- retraining model;
- fitting model;
- scraping;
- fitur pembelian laptop;
- checkout;
- payment gateway;
- database dari sisi frontend;
- data dummy sebagai sumber runtime;
- perubahan di luar folder `frontend/`;
- perubahan di folder `backend/`.

Fitur berikut diperbolehkan karena termasuk scope baru:

- login admin;
- autentikasi admin;
- validasi sesi admin;
- dashboard admin sederhana;
- protected route admin;
- CRUD laptop admin melalui API backend.

## Label Kebutuhan Laptop

Jangan mengubah, menerjemahkan, mengganti kapitalisasi, menambah, atau menghapus label kategori kebutuhan berikut:

- `Administrasi/Perkantoran`
- `Programming`
- `Desain Grafis`
- `Editing Video`

Ketentuan:

- Label publik dan admin harus konsisten dengan backend.
- Kategori laptop admin tidak boleh dipilih manual oleh frontend.
- Frontend tidak boleh menghitung kategori.
- Frontend hanya boleh menampilkan kategori hasil prediksi dari backend.

## Integrasi Backend API

- Ambil base URL dari environment variable `VITE_API_BASE_URL`.
- Gunakan fallback `http://127.0.0.1:8000` jika environment variable tidak tersedia.
- Semua request API wajib melalui service layer di `src/services/`.
- Jangan melakukan `fetch` langsung di page, component, layout, atau hook jika dapat dipisahkan ke service.
- CRUD admin wajib menggunakan service layer.
- Data utama aplikasi wajib berasal dari backend API, bukan data dummy.
- Gunakan nilai `success`, `message`, dan `data` sesuai response backend.
- Jika backend mengirim `success: false`, tampilkan pesan error dari backend.
- Jika request gagal, tampilkan pesan error yang jelas dan mudah dipahami.
- Jangan menyembunyikan error API dengan data dummy.

Format response backend:

```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```

## Endpoint Admin yang Harus Digunakan

Gunakan endpoint admin berikut sesuai kebutuhan frontend:

- `POST /api/admin/auth/login`
- `GET /api/admin/auth/me`
- `GET /api/admin/laptops`
- `GET /api/admin/laptops/{laptop_id}`
- `POST /api/admin/laptops`
- `PUT /api/admin/laptops/{laptop_id}`
- `DELETE /api/admin/laptops/{laptop_id}`

Ketentuan:

- Semua endpoint admin selain login wajib memakai Bearer token.
- Header autentikasi harus berbentuk `Authorization: Bearer <token>`.
- Jangan membuat endpoint admin baru dari sisi frontend.
- Jangan mengubah kontrak endpoint backend.
- Sorting hanya diterapkan jika backend mendukung parameter sorting.
- Pagination harus mengikuti response atau parameter backend.
- Search dan filter harus mengikuti parameter backend.

## Autentikasi Admin dan Token

- Token harus dikelola melalui service atau helper terpusat.
- Jangan menyebarkan logic penyimpanan token ke banyak component.
- Password tidak boleh disimpan di localStorage, sessionStorage, state global persisten, atau log.
- Access token tidak boleh dicetak ke console.
- Access token tidak boleh dimasukkan ke URL.
- Jangan menampilkan token di UI.
- Jangan menyimpan data sensitif yang tidak diperlukan.
- Response `401` dari endpoint admin harus menghapus sesi admin dan mengarahkan ke halaman login admin.
- Logout harus menghapus token dan state sesi admin.
- Protected route harus memvalidasi sesi melalui backend, misalnya memakai `GET /api/admin/auth/me`.
- Jangan menampilkan konten admin sebelum sesi tervalidasi.
- Tampilkan loading state saat validasi sesi berlangsung.
- Tampilkan error atau redirect yang jelas jika sesi tidak valid.
- Jangan mengandalkan proteksi frontend sebagai satu-satunya keamanan. Backend tetap sumber otorisasi utama.

## Route yang Disarankan

Route publik lama harus tetap tersedia:

- `/`
- `/recommendation`
- `/laptops`
- `/about`
- `*`

Route admin yang disarankan:

- `/admin/login`
- `/admin`
- `/admin/laptops`
- `/admin/laptops/create`
- `/admin/laptops/:id`
- `/admin/laptops/:id/edit`

Ketentuan routing:

- Route admin selain login harus dilindungi protected route.
- Login admin tidak boleh tampil untuk admin yang sesinya masih valid, kecuali ada kebutuhan UX yang jelas.
- Area admin harus memakai layout admin yang terpisah dari layout publik jika struktur UI berbeda.
- Navigasi publik lama jangan rusak karena penambahan route admin.

## Struktur Project

Gunakan struktur yang bersih, modular, dan sesuai tanggung jawab:

```text
src/
  components/
    elements/
    fragments/
    layouts/
  hooks/
  pages/
  services/
  styles/
    index.css
  utils/
```

Ketentuan struktur:

- `src/components/elements/`: komponen kecil dan reusable, seperti `Button`, `Input`, `Select`, `Badge`, `Card`, `Loading`, `EmptyState`, `ErrorState`, modal, dialog, dan notifikasi.
- `src/components/fragments/`: komponen gabungan, seperti `Navbar`, `HeroSection`, `RecommendationForm`, `RecommendationResult`, `LaptopCard`, `FilterSection`, `AdminSidebar`, `AdminHeader`, `AdminLaptopTable`, dan form fragment admin.
- `src/components/layouts/`: layout halaman atau wrapper struktur utama, termasuk `MainLayout` dan `AdminLayout`.
- `src/pages/`: komponen halaman publik dan admin.
- `src/services/`: konfigurasi dan fungsi request API, termasuk service autentikasi admin dan CRUD laptop admin.
- `src/utils/`: helper murni, formatter, constants, token helper, dan utilitas kecil.
- `src/hooks/`: custom React hooks, termasuk hook sesi admin, list admin, detail admin, dan mutasi admin jika diperlukan.
- `src/styles/index.css`: CSS utama aplikasi.

Pisahkan logic yang dapat digunakan ulang dari komponen. Page bertugas menyusun alur halaman, bukan menampung seluruh logic API dan tampilan dalam satu file besar.

## Aturan Service Layer

- Semua request publik dan admin harus melalui `src/services/`.
- `apiClient` atau client terpusat harus menangani base URL, parsing JSON, error response, dan header umum.
- Token admin harus ditambahkan oleh client/service terpusat, bukan manual berulang di tiap page.
- Service autentikasi admin harus menangani login, get current admin, logout, dan pembersihan sesi.
- Service laptop admin harus menangani list, detail, create, update, delete/nonaktifkan.
- Jangan membuat request langsung dari component kecil.
- Hook boleh memanggil service.
- Page boleh memanggil hook atau service jika logic sangat spesifik, tetapi pola reusable lebih baik diletakkan di hook.

## Form Laptop Admin

- Form laptop harus mengikuti schema backend final.
- Jangan membuat field yang tidak ada dalam kontrak backend.
- Jangan mengirim field kategori manual.
- Kategori tidak boleh dipilih manual.
- Frontend tidak boleh menghitung kategori.
- Frontend tidak boleh membuat confidence sendiri.
- Nilai enum harus diambil dari `/api/options` jika sesuai.
- Validasi frontend boleh dilakukan untuk UX, tetapi validasi backend tetap sumber kebenaran.
- Tampilkan error validasi backend dengan jelas.
- Field numerik tidak boleh mengirim nilai negatif jika schema melarangnya.
- Field kosong harus mengikuti aturan backend, bukan diisi dummy.
- Setelah create atau update berhasil, tampilkan `predicted_category` dari backend.
- Tampilkan `prediction_confidence` hanya jika backend mengirimkannya.
- Jika backend tidak mengirim confidence, jangan tampilkan nilai palsu, jangan tampilkan `100%`, dan jangan membuat fallback numerik.

## Data Laptop Admin

Daftar laptop admin harus mendukung jika backend menyediakan:

- search;
- filter;
- sorting;
- pagination;
- status aktif/nonaktif;
- sumber data;
- kategori hasil prediksi;
- confidence prediksi jika tersedia.

Ketentuan UI:

- Tampilkan loading saat data dimuat.
- Tampilkan error state saat request gagal.
- Tampilkan empty state saat data kosong.
- Gunakan dialog konfirmasi sebelum hapus atau nonaktifkan laptop.
- Tampilkan notifikasi sukses atau gagal setelah aksi penting.
- Jangan menghapus item dari UI sebelum backend mengonfirmasi keberhasilan, kecuali memakai optimistic update dengan rollback yang jelas.
- Detail laptop harus memakai data dari backend.
- Jangan memakai dummy data sebagai isi tabel, card, detail, atau form.

## Prediksi Kategori dan Confidence

- `predicted_category` harus berasal dari backend.
- `prediction_confidence` hanya ditampilkan jika backend mengirimkannya.
- Frontend tidak boleh menghitung confidence.
- Frontend tidak boleh menebak kategori dari spesifikasi.
- Frontend tidak boleh membuat kategori fallback.
- Jika field prediksi kosong atau tidak tersedia, tampilkan state yang jujur seperti `Belum tersedia` atau `-` sesuai pola UI.
- Jangan menyebut confidence sebagai kepastian mutlak.

## Aturan React

- Gunakan functional components dan React hooks.
- Buat komponen kecil dengan tanggung jawab yang jelas.
- Hindari duplikasi state, logic, dan markup.
- Letakkan logic request yang reusable di service atau custom hook.
- Gunakan nama komponen, props, state, dan fungsi yang jelas.
- Pastikan list memiliki key yang stabil.
- Jaga JSX tetap ringkas, bersih, dan mudah dibaca.
- Jangan mencampur logic autentikasi, fetch data, dan markup besar dalam satu component jika bisa dipisahkan.
- Jangan membuat state global berat jika kebutuhan dapat dipenuhi dengan hook/context sederhana.
- Gunakan context admin hanya jika membantu mengelola sesi dan data admin secara terpusat.

## Tailwind CSS v4 dan Styling

- Gunakan Tailwind CSS v4 melalui plugin `@tailwindcss/vite`.
- Gunakan `@import "tailwindcss";` di `src/styles/index.css`.
- Jangan menggunakan pola konfigurasi Tailwind v3 yang bergantung pada `tailwind.config.js` jika tidak diperlukan.
- Hindari `className` yang panjang, berulang, dan sulit dibaca di JSX.
- Jika sekumpulan style sering digunakan, buat class komponen yang reusable di CSS utama.
- Gunakan CSS modern dengan `@layer base`, `@layer components`, dan `@layer utilities`.
- Gunakan nama class yang jelas, misalnya `btn`, `btn-primary`, `card`, `input-field`, `select-field`, `section`, `page-shell`, `result-grid`, `admin-shell`, `admin-card`, `admin-table`, dan `admin-form`.
- Jangan menggunakan inline style kecuali benar-benar diperlukan.
- Pertahankan tampilan responsif dan aksesibel.
- Admin interface harus responsive untuk desktop, tablet, dan mobile.
- Jangan merusak styling area publik saat menambahkan styling area admin.

Contoh pola CSS yang dianjurkan:

```css
@import "tailwindcss";

@layer base {
  /* Global element defaults */
}

@layer components {
  .btn {
    /* Reusable button styles */
  }

  .btn-primary {
    /* Primary button variant */
  }
}

@layer utilities {
  /* Project-specific utilities only when needed */
}
```

## Kualitas UX dan Aksesibilitas

- Berikan label yang jelas untuk setiap input.
- Gunakan elemen HTML semantik.
- Pastikan tombol dan kontrol form dapat digunakan dengan keyboard.
- Tampilkan status loading selama request berlangsung dan cegah submit berulang bila diperlukan.
- Tampilkan `EmptyState` saat data tidak tersedia.
- Tampilkan `ErrorState` saat request gagal.
- Pertahankan pesan backend yang relevan agar pengguna memahami hasil rekomendasi atau aksi admin.
- Gunakan dialog konfirmasi untuk aksi destruktif.
- Notifikasi harus jelas, singkat, dan tidak menutupi informasi penting.
- Jangan hanya mengandalkan warna untuk menyampaikan status.
- Pastikan focus state tetap terlihat.
- Pastikan layout admin tetap usable pada layar kecil.

## Error Handling

Tangani kondisi berikut:

- backend belum aktif;
- endpoint tidak tersedia;
- response `success: false`;
- response `401`;
- response `403`;
- response `404`;
- validasi form gagal;
- token tidak valid;
- sesi admin kedaluwarsa;
- data laptop kosong;
- detail laptop tidak ditemukan;
- create laptop gagal;
- update laptop gagal;
- delete/nonaktifkan laptop gagal;
- options belum tersedia;
- model info belum tersedia;
- network error.

Jangan menampilkan stack trace mentah, token, password, atau detail internal yang sensitif kepada user.

## Testing dan Verifikasi Frontend

Tambahkan atau perbarui test yang relevan jika project memiliki setup testing.

Testing minimal untuk area admin:

- login berhasil;
- login gagal;
- protected route;
- token tidak valid;
- logout;
- daftar laptop admin;
- search laptop admin;
- filter laptop admin;
- sorting jika backend mendukung;
- pagination;
- detail laptop;
- tambah laptop;
- edit laptop;
- hapus atau nonaktifkan laptop;
- dialog konfirmasi;
- loading state;
- error state;
- empty state;
- notifikasi sukses/gagal;
- `predicted_category` berasal dari backend;
- `prediction_confidence` hanya tampil jika backend mengirimkannya.

Testing minimal untuk area publik:

- halaman publik lama tetap berjalan;
- beranda dapat dirender;
- form rekomendasi tetap dapat digunakan;
- hasil rekomendasi tampil dari backend;
- hasil alternatif tetap jelas;
- data laptop publik tetap tampil;
- about/model info tetap tampil;
- not found tetap tampil.

Verifikasi build:

- Jalankan lint jika script tersedia.
- Jalankan build frontend jika script tersedia.
- Pastikan build frontend berhasil sebelum menyatakan selesai, kecuali ada alasan spesifik yang menghalangi.

Contoh:

```bash
npm run lint
npm run build
```

Jika PowerShell memblokir `npm`, gunakan:

```bash
npm.cmd run lint
npm.cmd run build
```

## Checklist Sebelum Selesai

- Semua file yang berubah berada di dalam `frontend/`.
- Tidak ada perubahan di `backend/`.
- Tidak ada perubahan di luar `frontend/`.
- Area publik lama tetap berjalan.
- Route publik lama tetap tersedia.
- Route admin mengikuti protected route.
- Login admin tersedia jika diminta implementasi.
- Token dikelola terpusat.
- Password tidak disimpan.
- Token tidak dicetak ke console.
- Response `401` membersihkan sesi dan mengarahkan ke login admin.
- Konten admin tidak tampil sebelum sesi tervalidasi.
- Semua request API melalui service layer.
- CRUD laptop admin melalui service layer.
- Form laptop mengikuti schema backend final.
- Kategori tidak dipilih manual.
- Frontend tidak menghitung kategori.
- Frontend tidak membuat confidence sendiri.
- Enum diambil dari `/api/options` jika sesuai.
- `predicted_category` ditampilkan dari backend.
- `prediction_confidence` hanya tampil jika backend mengirim.
- Loading, error, dan empty state tersedia.
- Dialog konfirmasi tersedia untuk aksi hapus/nonaktifkan.
- Notifikasi tersedia untuk aksi penting.
- Responsive design publik dan admin terjaga.
- Tailwind CSS v4 tetap digunakan.
- Tidak ada dummy data sebagai sumber runtime.
- Empat label kebutuhan tetap persis.
- Lint dan build dijalankan jika tersedia.
- File yang diubah dan hasil verifikasi dilaporkan secara ringkas.
