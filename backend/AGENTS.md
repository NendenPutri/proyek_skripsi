# Backend Agent Instructions

## Scope Kerja

- Kerjakan seluruh perubahan backend hanya di dalam folder `backend/`.
- Jangan membuat, mengubah, memindahkan, atau menghapus file di `frontend/`.
- Jangan membuat, mengubah, memindahkan, atau menghapus file di luar folder `backend/`.
- Untuk tahap instruksi ini, jangan mulai implementasi fitur kecuali pengguna secara eksplisit meminta implementasi.
- Backend dibuat dengan FastAPI dan wajib dapat dijalankan dari folder `backend/` menggunakan:

  ```bash
  fastapi dev main.py
  ```

- Backend melayani API yang dikonsumsi frontend ReactJS.
- Backend menggunakan dataset CSV, options JSON, metadata model, pipeline Joblib, dan MySQL.
- Backend menggunakan SQLAlchemy ORM untuk akses database.
- Backend menggunakan Alembic untuk migration database.
- Backend menyediakan area publik untuk pengguna umum dan area admin dari sisi API.
- Baca struktur, pola route, schema, service, konfigurasi, database, migration, dan testing yang sudah ada sebelum melakukan perubahan.
- Pertahankan endpoint, response field, business logic, dan fitur lama yang masih digunakan frontend.
- Jangan menghapus atau mengganti fitur lama hanya karena fitur admin, database, atau CRUD ditambahkan.
- Penambahan autentikasi, database, migration, repository, dan CRUD admin harus modular.
- Jangan melakukan perubahan apa pun di luar kebutuhan backend sistem rekomendasi laptop.

## Tujuan Sistem

Backend menyediakan rekomendasi pemilihan laptop berdasarkan kebutuhan pengguna dengan algoritma utama Naive Bayes.

Backend memiliki dua area utama:

- Area publik untuk pengguna umum.
- Area admin untuk mengelola data laptop.

Area publik menyediakan:

- status backend;
- pilihan input dan filter;
- daftar laptop;
- rekomendasi laptop;
- informasi model.

Area admin menyediakan:

- login admin;
- validasi sesi admin;
- endpoint dashboard data dari sisi API;
- daftar laptop admin;
- tambah laptop manual;
- edit laptop;
- hapus atau nonaktifkan laptop;
- prediksi kategori laptop baru menggunakan pipeline Naive Bayes.

Backend hanya melakukan inferensi menggunakan model yang sudah dilatih.

Jangan melakukan:

- training ulang dari backend;
- preprocessing dataset mentah;
- scraping;
- upload dataset;
- upload model;
- upload CSV;
- import CSV melalui dashboard;
- fitting model saat request berlangsung.

Data laptop baru yang dimasukkan admin harus:

- divalidasi;
- dinormalisasi;
- disesuaikan dengan fitur model;
- diproses menggunakan pipeline Naive Bayes;
- memperoleh kategori hasil prediksi;
- memperoleh confidence jika pipeline mendukung `predict_proba()`;
- disimpan ke MySQL;
- tersedia pada daftar laptop publik jika aktif;
- tersedia dalam proses rekomendasi jika aktif.

## Perbedaan Training dan Inferensi

Model Naive Bayes telah dilatih menggunakan dataset berlabel.

Backend tidak boleh menjalankan proses berikut saat admin menambahkan atau mengubah laptop:

```python
model.fit(...)
```

Backend juga tidak boleh menjalankan:

```python
model.partial_fit(...)
```

Backend hanya menggunakan model yang sudah dilatih untuk inferensi:

```python
model.predict(...)
```

Jika pipeline mendukung probabilitas, backend boleh menggunakan:

```python
model.predict_proba(...)
```

Ketentuan:

- Laptop baru tidak perlu dimasukkan ke training untuk dapat diprediksi.
- Laptop baru tidak boleh otomatis ditambahkan ke dataset training.
- Laptop baru tidak boleh memicu retraining otomatis.
- Retraining hanya dilakukan secara terpisah jika diminta eksplisit.
- Data baru harus melewati preprocessing yang tersimpan dalam pipeline model.
- Jangan membuat encoder baru saat runtime.
- Jangan melakukan fitting encoder pada data baru.

## Artefak Sumber Data

Artefak berikut ditempatkan di backend dan tetap digunakan sebagai sumber data utama:

- `data/laptops_backend_ready.csv`: dataset final laptop yang siap digunakan backend.
- `data/frontend_options.json`: pilihan dan filter yang disediakan kepada frontend.
- `models/naive_bayes_laptop_pipeline.joblib`: pipeline model Naive Bayes untuk inferensi.
- `models/model_metadata.json`: metadata model.

Ketentuan penggunaan artefak:

- Jangan mengganti artefak dengan dummy data sebagai sumber data utama.
- Jangan menghapus artefak setelah database ditambahkan.
- Jangan mengubah isi artefak kecuali pengguna secara eksplisit meminta perubahan tersebut.
- Gunakan path yang dihitung relatif terhadap lokasi backend.
- Jangan bergantung pada current working directory yang tidak pasti.
- Muat dan validasi file secara aman.
- Berikan error yang jelas dan konsisten jika file belum tersedia, tidak dapat dibaca, rusak, atau formatnya tidak sesuai.
- Jangan memuat ulang dataset atau model pada setiap request jika dapat dimuat sekali dan digunakan kembali dengan aman.
- Jangan menulis data admin ke file CSV.
- Jangan memperbarui CSV saat runtime.
- Jangan mengganti file model saat request berlangsung.
- Jangan memakai fixture atau dummy data sebagai fallback produksi.
- Jangan menyembunyikan kegagalan artefak dengan data buatan.

## Sumber Data Sistem

Backend menggunakan dua sumber data.

### Dataset CSV

Dataset CSV digunakan untuk:

- sumber data laptop awal;
- katalog laptop lama;
- kandidat awal rekomendasi;
- referensi struktur data;
- data yang sudah melalui preprocessing.

CSV tidak boleh diubah saat runtime.

### Database MySQL

MySQL digunakan untuk menyimpan:

- akun admin;
- laptop yang ditambahkan admin;
- laptop yang diubah admin;
- kategori hasil prediksi;
- confidence jika model mendukung;
- status aktif laptop;
- sumber data;
- waktu dibuat;
- waktu diperbarui.

MySQL tidak digunakan untuk:

- training model;
- menyimpan file model;
- menggantikan pipeline Joblib;
- preprocessing dataset mentah;
- menyimpan data CSV hasil penggabungan.

## Penggabungan Data CSV dan MySQL

Data laptop publik berasal dari gabungan:

```text
CSV hasil preprocessing
        +
Data laptop aktif dari MySQL
        |
        v
Service backend
        |
        v
Daftar laptop dan rekomendasi
```

Ketentuan:

- Samakan schema data dari CSV dan MySQL.
- Samakan nama field yang dikembalikan API publik.
- Samakan tipe data dan format nilai.
- Jangan mengubah field yang sudah digunakan frontend tanpa permintaan eksplisit.
- Data MySQL yang tidak aktif tidak boleh tampil pada endpoint publik.
- Data MySQL yang tidak aktif tidak boleh masuk rekomendasi.
- Hindari duplikasi laptop.
- Jangan menulis hasil penggabungan kembali ke CSV.
- Jangan memuat ulang CSV berulang jika sudah tersedia di memory.
- Jangan menyimpan seluruh database ke memory tanpa kebutuhan.
- Filtering harus konsisten untuk data CSV dan MySQL.
- Sorting harus konsisten untuk data CSV dan MySQL.
- Pagination harus konsisten untuk data CSV dan MySQL.
- Data MySQL dapat diprioritaskan jika memiliki brand dan model yang sama dengan data CSV.
- Aturan prioritas data harus jelas dan terdokumentasi.
- Data CSV tidak wajib dimigrasikan ke MySQL.
- Jika migrasi dilakukan, proses harus eksplisit, idempotent, dan tidak berjalan otomatis tanpa instruksi.

## Label Kebutuhan

Gunakan label berikut secara persis. Jangan menerjemahkan, mengganti nama, mengubah kapitalisasi, atau menambahkan label baru:

- `Administrasi/Perkantoran`
- `Programming`
- `Desain Grafis`
- `Editing Video`

Ketentuan:

- Kategori hasil prediksi harus salah satu dari empat label tersebut.
- Jangan menyimpan kategori lain.
- Jangan membuat kategori fallback buatan.
- Jangan mengubah label agar sesuai selera implementasi.
- Jangan menentukan kategori melalui aturan frontend.
- Kategori laptop baru berasal dari model backend.

## Alur Data Laptop Baru dari Admin

Ketika admin menambahkan laptop secara manual, gunakan alur berikut:

```text
Admin mengirim spesifikasi laptop
        |
        v
Validasi request menggunakan Pydantic
        |
        v
Normalisasi data
        |
        v
Bentuk fitur sesuai pipeline
        |
        v
Jalankan model.predict()
        |
        v
Gunakan model.predict_proba() hanya jika tersedia
        |
        v
Validasi hasil kategori
        |
        v
Simpan data dan hasil prediksi ke MySQL
        |
        v
Laptop aktif tersedia pada endpoint publik dan rekomendasi
```

Ketentuan:

- Data hanya disimpan setelah validasi dan inferensi berhasil.
- Jangan menyimpan data parsial.
- Gunakan transaksi database.
- Jika inferensi gagal, rollback transaksi.
- Jika validasi kategori gagal, rollback transaksi.
- Jangan mengarang kategori.
- Jangan menggunakan kategori default.
- Jangan melakukan training ulang.
- Jangan menambahkan data ke CSV.
- Jangan mengubah file Joblib.
- Gunakan metadata model untuk memvalidasi fitur jika tersedia.
- Konversikan tipe NumPy, Pandas, dan nilai `NaN` ke tipe Python atau `None` sebelum response dan penyimpanan.

## Fitur Model dan Preprocessing

- Algoritma utama harus tetap Naive Bayes melalui pipeline Joblib yang disediakan.
- Jangan mengganti algoritma.
- Jangan melatih model dari backend.
- Jangan melakukan fitting.
- Jangan melakukan retraining otomatis.
- Pastikan fitur yang dikirim ke model sesuai dengan nama fitur, urutan fitur, tipe data, nilai kategori, dan metadata model.
- Jangan menentukan struktur fitur secara sembarangan.
- Jangan melakukan encoding yang bertentangan dengan pipeline.
- Jangan membuat preprocessing baru jika pipeline sudah menyediakannya.
- Jangan mengubah mapping fitur tanpa permintaan eksplisit.
- Tangani nilai kategori yang tidak dikenal dengan error yang jelas.
- Tangani versi model yang tidak kompatibel.
- Tangani fitur hilang.
- Tangani tipe data yang salah.
- Tangani kegagalan inferensi.

Fitur model yang sudah digunakan pipeline saat ini harus dipertahankan kecuali metadata model berubah secara eksplisit:

- `brand_name`
- `processor_brand`
- `processor_series`
- `processor_level`
- `ram_class`
- `memory_type`
- `storage_class`
- `gpu_brand`
- `gpu_type`
- `gpu_level`
- `os_family`
- `display_class`
- `resolution_class`
- `touchscreen_label`
- `warranty_class`
- `price_class`

## Confidence Prediksi

Gunakan confidence hanya jika pipeline mendukung `predict_proba()`.

Jika tersedia:

- ambil probabilitas kelas hasil prediksi;
- ubah tipe NumPy menjadi tipe Python;
- simpan sebagai nilai numerik yang valid;
- jangan menyebut confidence sebagai kepastian mutlak.

Jika tidak tersedia:

- jangan membuat confidence buatan;
- jangan memakai nilai default palsu;
- gunakan `null` jika schema menyediakan field confidence.

## Endpoint Publik Wajib

Implementasikan dan pertahankan endpoint berikut:

### `GET /api/health`

Fungsi:

- status layanan;
- status database;
- kesiapan dataset;
- kesiapan model;
- kesiapan frontend options;
- kesiapan metadata model.

Health endpoint harus menjelaskan komponen yang siap, tidak siap, atau gagal dimuat.

### `GET /api/options`

Fungsi:

- mengambil pilihan input dan filter dari `frontend_options.json`;
- menyediakan enum untuk form publik;
- menyediakan enum untuk form admin jika sesuai.

### `GET /api/laptops`

Fungsi:

- mengambil daftar laptop dari CSV dan MySQL;
- menggabungkan kedua sumber;
- memvalidasi query parameter;
- mendukung search;
- mendukung filter;
- mendukung pagination;
- mendukung sorting jika diperlukan;
- hanya menampilkan data aktif dari MySQL.

### `POST /api/recommendations`

Fungsi:

- memvalidasi input pengguna;
- menjalankan inferensi model;
- memilih kandidat laptop dari CSV dan MySQL;
- melakukan filter;
- melakukan ranking;
- mengembalikan rekomendasi utama;
- mengembalikan rekomendasi alternatif jika diperlukan.

### `GET /api/model-info`

Fungsi:

- mengambil informasi model yang aman dari `model_metadata.json`;
- tidak membocorkan object model;
- tidak membocorkan path lokal;
- tidak membocorkan detail sensitif.

Jangan mengubah nama endpoint publik tanpa permintaan eksplisit.

Jangan mengubah nama field response yang sudah digunakan frontend tanpa permintaan eksplisit.

## Endpoint Autentikasi Admin

Tambahkan dan pertahankan endpoint berikut:

### `POST /api/admin/auth/login`

Fungsi:

- menerima email atau username;
- menerima password;
- memvalidasi kredensial;
- memeriksa status aktif admin;
- menghasilkan JWT access token.

Ketentuan:

- Jangan mengembalikan password.
- Jangan mengembalikan password hash.
- Jangan membocorkan apakah akun tertentu tersedia.
- Gunakan pesan login gagal yang umum, misalnya `Email/username atau password tidak valid.`

### `GET /api/admin/auth/me`

Fungsi:

- memvalidasi JWT access token;
- mengambil data admin yang sedang login;
- memastikan admin masih aktif.

Endpoint ini wajib dilindungi autentikasi.

Jangan membuat endpoint register admin publik.

## Endpoint Pengelolaan Laptop Admin

Tambahkan dan pertahankan endpoint berikut:

### `GET /api/admin/laptops`

Fungsi:

- mengambil daftar laptop admin;
- mendukung search;
- mendukung filter;
- mendukung sorting;
- mendukung pagination;
- menampilkan status aktif;
- menampilkan sumber data;
- menampilkan kategori hasil prediksi.

### `GET /api/admin/laptops/{laptop_id}`

Fungsi:

- mengambil detail laptop;
- mengembalikan `404` jika data tidak ditemukan.

### `POST /api/admin/laptops`

Fungsi:

- menerima data laptop manual;
- memvalidasi payload;
- menjalankan inferensi;
- menyimpan hasil ke MySQL;
- mengembalikan kategori hasil prediksi.

### `PUT /api/admin/laptops/{laptop_id}`

Fungsi:

- memperbarui seluruh data laptop;
- melakukan inferensi ulang jika fitur model berubah;
- mempertahankan kategori jika hanya field non-model berubah;
- menggunakan transaksi.

### `DELETE /api/admin/laptops/{laptop_id}`

Fungsi:

- menghapus atau menonaktifkan laptop;
- mengutamakan soft delete atau status aktif jika data perlu dipertahankan;
- mengembalikan response yang jelas.

### `PATCH /api/admin/laptops/{laptop_id}`

- Buat hanya jika benar-benar diperlukan.
- Jangan membuat PUT dan PATCH dengan logic duplikat.
- Jangan memaksakan PATCH jika tidak digunakan frontend atau kebutuhan API.

Semua endpoint `/api/admin/*` selain login wajib menggunakan autentikasi admin.

## Input Laptop Admin

Input laptop admin dilakukan melalui form manual.

Field harus mengikuti schema backend dan struktur data sistem.

Field dapat mencakup:

- `brand`
- `brand_name`
- `model`
- `price`
- `ram`
- `ram_num`
- `storage`
- `memory_size`
- `memory_type`
- `processor`
- `processor_brand`
- `processor_series`
- `processor_level`
- `gpu`
- `gpu_brand`
- `gpu_type`
- `gpu_level`
- `os_family`
- `touch_screen`
- `touchscreen_label`
- `screen_size`
- `rating`
- field lain yang memang tersedia pada dataset atau kontrak API.

Ketentuan:

- Jangan membuat field yang tidak diperlukan.
- Bedakan field katalog dan field model.
- Nama laptop dapat disimpan walaupun tidak menjadi fitur model.
- Gunakan enum untuk nilai terbatas.
- Gunakan pilihan dari `frontend_options.json` jika sesuai.
- Tolak field wajib yang kosong.
- Tolak nilai harga negatif.
- Tolak RAM negatif.
- Tolak storage negatif.
- Tolak rating di luar rentang.
- Tolak tipe data yang tidak sesuai.
- Normalisasi boolean.
- Normalisasi kategori.
- Hindari duplikasi.
- Kombinasi brand dan model dapat digunakan sebagai kandidat aturan unik.
- Jangan membuat upload CSV.
- Jangan membuat import CSV.
- Jangan membuat endpoint upload file.

## Aturan Pembaruan Laptop

Jika admin mengubah field yang digunakan model, jalankan inferensi ulang.

Field yang mungkin memengaruhi model:

- brand;
- harga;
- RAM;
- storage;
- processor brand;
- processor series;
- processor level;
- memory type;
- GPU brand;
- GPU type;
- GPU level;
- sistem operasi;
- display class;
- resolution class;
- touch screen;
- warranty class;
- price class;
- field lain yang terdaftar pada metadata model.

Jika admin hanya mengubah field non-model seperti gambar, deskripsi, nama tampilan tambahan, atau informasi katalog, inferensi ulang tidak wajib.

Ketentuan:

- Jangan menebak daftar fitur jika metadata tersedia.
- Gunakan metadata dan pipeline.
- Jika inferensi ulang gagal, rollback perubahan.
- Jangan menyimpan kategori lama jika fitur utama berubah tetapi inferensi baru gagal.

## Struktur dan Arsitektur

- Gunakan struktur yang clean dan modular.
- Pertahankan `main.py` sebagai entry point yang ringkas.
- `main.py` hanya digunakan untuk membuat aplikasi, memasang middleware, mendaftarkan router, mengatur lifecycle, dan menghubungkan konfigurasi utama.

Jangan menumpuk di `main.py`:

- route handler;
- business logic;
- query database;
- pembacaan file;
- transformasi data;
- autentikasi;
- hashing password;
- inferensi model.

Pisahkan tanggung jawab ke modul yang sesuai:

### `api/` atau `routes/`

Digunakan untuk endpoint publik, endpoint autentikasi admin, dan endpoint pengelolaan laptop admin.

Route hanya menangani request, dependency, status code, response, dan pemanggilan service.

### `schemas/`

Digunakan untuk request Pydantic, response Pydantic, schema autentikasi, schema laptop, schema rekomendasi, schema pagination, dan validasi input.

### `services/`

Digunakan untuk business logic, pembacaan dataset, inferensi model, penyusunan rekomendasi, autentikasi, penggabungan data, dan pengelolaan laptop.

### `repositories/`

Digunakan untuk akses database, query admin, query laptop, pagination, search, filter, dan operasi CRUD.

### `db/`

Digunakan untuk engine, session, base ORM, dependency database, dan konfigurasi database.

### `models/` atau `db/models/`

Digunakan untuk model ORM.

Jangan mencampurkan model ORM dengan file model machine learning tanpa penamaan yang jelas.

### `core/`

Digunakan untuk konfigurasi, konstanta, lifecycle, security, logging, dan dependency bersama.

### `utils/`

Gunakan hanya untuk helper generik yang benar-benar dipakai.

### `tests/`

Digunakan untuk unit test dan integration test.

Hindari abstraksi berlebihan. Ikuti pola backend yang sudah ada jika project telah berkembang.

Gunakan type hints pada fungsi publik, service utama, repository, dependency, dan business logic penting.

## Struktur Database

Gunakan MySQL sebagai database utama.

Gunakan:

- SQLAlchemy untuk ORM;
- Alembic untuk migration;
- `DATABASE_URL` dari environment variable.

SQLite hanya boleh digunakan untuk test lokal jika test mengisolasi database dan tidak menggantikan konfigurasi MySQL aplikasi.

### Tabel Admin

Field minimal:

- `id`
- `name`
- `email`
- `username` jika digunakan
- `password_hash`
- `is_active`
- `created_at`
- `updated_at`

Ketentuan:

- Email harus unik jika digunakan.
- Username harus unik jika digunakan.
- Password wajib disimpan dalam bentuk hash.
- Password hash tidak boleh dikembalikan.
- Admin nonaktif tidak boleh login.

### Tabel Laptop

Field minimal disesuaikan dengan schema project:

- `id`
- `brand_name`
- `model`
- `price`
- `ram_num`
- `memory_size`
- `memory_type`
- `processor_brand`
- `processor_series`
- `processor_level`
- `gpu_brand`
- `gpu_type`
- `gpu_level`
- `os_family`
- `touch_screen`
- `touchscreen_label`
- `rating`
- `predicted_label`
- `prediction_confidence`
- `source`
- `is_active`
- `created_at`
- `updated_at`

Ketentuan:

- `source` untuk data admin menggunakan nilai konsisten seperti `admin`.
- Jangan menyimpan `NaN`.
- Jangan menyimpan tipe NumPy langsung.
- Jangan menyimpan tipe Pandas langsung.
- Konversikan ke tipe Python.
- Gunakan tipe database yang tepat.
- Gunakan migration untuk perubahan schema.
- Data admin tidak ditulis ke CSV.
- Data CSV tidak harus dimigrasikan ke database.

## Migration Database

- Gunakan Alembic.
- Jangan hanya mengandalkan `create_all()` untuk production.
- `create_all()` boleh digunakan sementara untuk development awal jika diberi catatan jelas.
- Sediakan migration tabel admin.
- Sediakan migration tabel laptop.
- Setiap perubahan schema harus memiliki migration.
- Jangan menghapus data otomatis.
- Jangan membuat migration destruktif tanpa instruksi jelas.
- Verifikasi migration dapat dijalankan.

## Inisialisasi Admin

Sediakan cara aman untuk membuat admin pertama.

Cara yang diperbolehkan:

- seeder;
- script internal;
- command CLI;
- bootstrap melalui environment variable.

Ketentuan:

- Jangan membuat register admin publik.
- Jangan memasukkan password nyata ke source code.
- Jangan membuat password default lemah.
- Jangan mencetak password ke log.
- Seeder harus idempotent jika memungkinkan.
- Jangan membuat akun duplikat setiap startup.

## Kontrak API dan Validasi

- Gunakan Pydantic untuk memvalidasi seluruh request body dan response.
- Definisikan `response_model` jika memungkinkan.
- Gunakan format response JSON yang konsisten.
- Jangan mengembalikan `NaN`, tipe NumPy, tipe Pandas, object ORM mentah, object model internal, atau data yang tidak diperlukan frontend.
- Validasi enum, filter, rentang numerik, pagination, sorting, search, input model, input admin, dan identifier data.
- Gunakan status code HTTP yang tepat.
- Jangan membocorkan stack trace, path lokal, query database, secret, atau detail internal model.
- Pertahankan kompatibilitas API dengan frontend.
- Jangan mengubah nama field response tanpa permintaan eksplisit.

Format sukses:

```json
{
  "success": true,
  "message": "Request berhasil diproses",
  "data": {}
}
```

Format error:

```json
{
  "success": false,
  "message": "Penjelasan error yang jelas",
  "data": null
}
```

Format pagination yang disarankan:

```json
{
  "success": true,
  "message": "Data berhasil diambil",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 0,
      "total_pages": 0
    }
  }
}
```

## Status Code

Gunakan status code yang tepat:

- `200` untuk request berhasil.
- `201` untuk data berhasil dibuat.
- `204` jika response tanpa body memang digunakan.
- `400` untuk request tidak valid secara business rule.
- `401` untuk autentikasi gagal.
- `403` untuk akses ditolak.
- `404` untuk data tidak ditemukan.
- `409` untuk konflik atau duplikasi.
- `422` untuk validasi schema.
- `500` untuk kegagalan internal.
- `503` untuk layanan atau dependency penting tidak siap jika sesuai.

## Aturan Rekomendasi dan Model

- Algoritma utama tetap Naive Bayes.
- Jangan mengganti algoritma.
- Jangan melakukan training.
- Jangan melakukan retraining.
- Jangan melakukan fitting.
- Gunakan pipeline Joblib.
- Pastikan fitur sesuai pipeline.
- Gunakan hasil prediksi model sebagai dasar kategori laptop baru.
- Gunakan hasil prediksi dan filter pengguna sebagai dasar rekomendasi.
- Pilih kandidat dari dataset CSV dan laptop aktif di MySQL.
- Ranking harus deterministik.
- Ranking harus dapat dijelaskan.
- Jangan mengarang probabilitas, skor, spesifikasi, harga, rating, laptop, kategori, atau alasan rekomendasi.
- Pertahankan perilaku rekomendasi alternatif jika sudah tersedia.

Jangan menghapus field berikut jika frontend menggunakannya:

- `is_alternative`
- `unmet_filters`
- `match_percentage`
- `is_exact_match`
- `alasan_rekomendasi`

## Konfigurasi dan Keamanan

- Simpan konfigurasi terpusat di `core/`.
- Jangan menyebarkan path dan konstanta ke banyak modul.
- Konfigurasi CORS harus terbatas pada kebutuhan frontend.
- Gunakan environment variable.
- Jangan mengeksekusi isi file sebagai kode.
- Jangan memasukkan secret ke source code.
- Jangan memasukkan credential database ke source code.
- Jangan memasukkan path mesin lokal.
- Jangan memasukkan password admin.
- Jangan memasukkan JWT secret.
- JWT secret tidak boleh di-hardcode.
- Password admin wajib disimpan dalam bentuk hash.

Environment minimal:

```env
APP_NAME=
APP_VERSION=
API_PREFIX=/api
DATABASE_URL=
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
BACKEND_CORS_ORIGINS=
```

Sediakan `.env.example` tanpa secret nyata.

## Autentikasi dan Keamanan Admin

- Gunakan JWT access token atau mekanisme token yang sesuai.
- Password harus di-hash menggunakan bcrypt atau Argon2.
- Jangan menyimpan password plaintext.
- JWT secret harus berasal dari environment variable.
- Token harus memiliki masa berlaku.
- Validasi status aktif admin.
- Gunakan FastAPI dependency untuk melindungi route admin.
- Jangan mengandalkan proteksi frontend.
- Semua otorisasi diperiksa di backend.
- Jangan mengembalikan token dalam URL.
- Jangan mencatat token penuh.
- Jangan mencatat password.
- Jangan mencatat password hash.
- Jangan mencatat credential database.
- Gunakan pesan login gagal yang aman.

## CORS

- CORS harus dapat dikonfigurasi melalui environment variable.
- Izinkan hanya origin frontend yang dibutuhkan.
- Jangan menggunakan wildcard di production tanpa alasan jelas.
- Pastikan header `Authorization` diizinkan.
- Pertahankan dukungan development lokal.

## Lifecycle Aplikasi

Pada startup:

- validasi konfigurasi;
- muat atau cek dataset;
- muat atau cek options;
- muat atau cek metadata;
- muat atau cek model;
- cek koneksi database;
- validasi artifact;
- siapkan dependency aplikasi.

Pada shutdown:

- tutup resource jika diperlukan;
- lepaskan koneksi dengan aman.

Jika artefak atau database gagal:

- catat error;
- tampilkan status pada health endpoint;
- jangan mengarang data;
- jangan menyembunyikan kegagalan.

## Logging

- Gunakan logging terstruktur.
- Jangan menggunakan `print()` untuk logging production.

Catat:

- startup;
- shutdown;
- status artefak;
- status database;
- kegagalan inferensi;
- kegagalan query;
- login gagal secara aman;
- operasi CRUD penting.

Jangan catat:

- password;
- token penuh;
- JWT secret;
- credential database;
- password hash;
- request sensitif secara utuh.

## Error Handling

Tangani kondisi berikut:

- model hilang;
- model rusak;
- CSV hilang;
- CSV rusak;
- frontend options hilang;
- metadata hilang;
- database tidak tersedia;
- migration gagal;
- login gagal;
- token tidak valid;
- token kedaluwarsa;
- admin tidak aktif;
- laptop tidak ditemukan;
- data duplikat;
- inferensi gagal;
- rollback saat inferensi gagal;
- fitur tidak sesuai;
- tipe data tidak sesuai;
- metadata tidak sesuai;
- dependency belum siap.

Jangan menampilkan detail internal langsung ke frontend.

## Testing dan Verifikasi

- Tambahkan atau perbarui test yang relevan ketika mengimplementasikan perilaku backend.
- Gunakan fixture atau mocking untuk test.
- Data fixture kecil boleh digunakan untuk testing.
- Fixture tidak boleh menjadi sumber runtime utama.
- Setelah perubahan, verifikasi aplikasi dapat diimpor dan dijalankan:

  ```bash
  fastapi dev main.py
  ```

Test minimal harus mencakup:

### Test Schema

- validasi request rekomendasi;
- validasi login admin;
- validasi tambah laptop;
- validasi edit laptop;
- enum tidak valid;
- nilai numerik negatif;
- field wajib kosong.

### Test Database dan Migration

- koneksi MySQL;
- konfigurasi `DATABASE_URL`;
- migration Alembic berjalan;
- tabel admin tersedia;
- tabel laptop tersedia;
- kondisi database gagal.

### Test Autentikasi

- login berhasil;
- login gagal;
- token valid;
- token tidak valid;
- token kedaluwarsa;
- tanpa token;
- admin tidak aktif;
- endpoint admin terlindungi.

### Test CRUD Laptop

- tambah laptop berhasil;
- prediksi kategori berhasil;
- data disimpan setelah inferensi;
- data tidak disimpan jika inferensi gagal;
- rollback saat inferensi gagal;
- edit laptop;
- inferensi ulang jika fitur berubah;
- tidak melakukan inferensi ulang jika field non-model berubah;
- hapus laptop;
- soft delete atau nonaktifkan laptop;
- duplikasi ditangani;
- data tidak ditemukan.

### Test Inferensi

- fitur model lengkap;
- fitur model hilang;
- kategori hasil prediksi valid;
- `predict()` berhasil;
- `predict_proba()` digunakan jika tersedia;
- `predict_proba()` tidak tersedia;
- kegagalan inferensi ditangani.

### Test Endpoint Publik

- `GET /api/health`;
- `GET /api/options`;
- `GET /api/laptops`;
- `POST /api/recommendations`;
- `GET /api/model-info`.

### Test Endpoint Admin

- `POST /api/admin/auth/login`;
- `GET /api/admin/auth/me`;
- `GET /api/admin/laptops`;
- `GET /api/admin/laptops/{laptop_id}`;
- `POST /api/admin/laptops`;
- `PUT /api/admin/laptops/{laptop_id}`;
- `DELETE /api/admin/laptops/{laptop_id}`;
- proteksi token pada semua endpoint admin selain login.

### Test Penggabungan Data

- data CSV tampil;
- data MySQL aktif tampil;
- data MySQL nonaktif tidak tampil;
- data MySQL aktif masuk rekomendasi;
- data MySQL nonaktif tidak masuk rekomendasi;
- duplikasi ditangani;
- schema konsisten;
- tipe data konsisten.

### Test Kondisi Gagal

- artefak hilang;
- artefak rusak;
- database gagal;
- metadata tidak sesuai;
- model gagal inferensi;
- fitur tidak dikenali.

Jangan menyatakan selesai jika:

- endpoint belum diuji;
- autentikasi belum diuji;
- migration belum diperiksa;
- inferensi laptop baru belum diuji;
- penggabungan CSV dan MySQL belum diuji;
- aplikasi gagal dijalankan.

Jika verifikasi terhalang, jelaskan keterbatasannya secara spesifik.

## Fitur yang Termasuk Scope Backend

Fitur berikut termasuk:

- FastAPI;
- MySQL;
- SQLAlchemy ORM;
- Alembic migration;
- akun admin;
- login admin;
- JWT access token;
- validasi sesi admin;
- proteksi endpoint admin;
- daftar laptop admin;
- tambah laptop manual;
- edit laptop;
- hapus atau nonaktifkan laptop;
- soft delete atau status aktif laptop;
- inferensi kategori laptop baru;
- confidence jika model mendukung;
- penyimpanan hasil prediksi ke MySQL;
- penggabungan CSV dan MySQL;
- data MySQL aktif masuk daftar publik;
- data MySQL aktif masuk rekomendasi;
- validasi;
- error handling;
- testing backend;
- dokumentasi endpoint backend jika diminta.

## Fitur yang Tidak Termasuk Scope Backend

Fitur berikut tidak termasuk kecuali diminta eksplisit:

- login pengguna umum;
- register pengguna umum;
- register admin publik;
- lupa password;
- reset password;
- verifikasi email;
- multi-role kompleks;
- upload CSV;
- import CSV;
- upload dataset;
- upload model;
- training model;
- retraining model;
- scraping;
- sinkronisasi marketplace;
- transaksi pembelian;
- payment gateway;
- notifikasi email;
- refresh token kompleks;
- audit log lengkap;
- hosting;
- domain;
- perubahan pada folder frontend;
- perubahan di luar folder backend.

## Batasan Tegas

Jangan membuat:

- login pengguna umum;
- register pengguna umum;
- register admin publik;
- upload CSV;
- import CSV dari dashboard;
- endpoint upload dataset;
- endpoint upload model;
- scraping;
- payment;
- transaksi pembelian;
- training;
- retraining;
- fitting model;
- dummy data sebagai sumber runtime;
- perubahan label kebutuhan;
- perubahan di luar folder `backend/`;
- perubahan di `frontend/`.

## Checklist Sebelum Selesai

- Semua file yang berubah berada di dalam `backend/`.
- Tidak ada perubahan di `frontend/`.
- Tidak ada perubahan di luar `backend/`.
- `main.py` tetap ringkas.
- Routes, schemas, services, repositories, database, core, dan utils dipisahkan sesuai tanggung jawab.
- Dataset CSV tetap digunakan.
- Pipeline Joblib tetap digunakan.
- Metadata model tetap digunakan.
- Frontend options tetap digunakan.
- MySQL terhubung melalui `DATABASE_URL`.
- SQLAlchemy ORM tersedia.
- Alembic migration tersedia.
- Tabel admin tersedia.
- Tabel laptop tersedia.
- Password admin disimpan dalam bentuk hash.
- Tidak ada password plaintext.
- JWT secret berasal dari environment variable.
- Login admin tersedia.
- Endpoint admin terlindungi.
- CRUD laptop tersedia.
- Tambah laptop menggunakan form manual.
- Tidak ada import CSV.
- Tidak ada upload CSV.
- Laptop baru diprediksi menggunakan pipeline Naive Bayes.
- Backend tidak menjalankan training ulang.
- Backend tidak menjalankan `fit()`.
- Backend tidak menjalankan `partial_fit()`.
- Data baru disimpan di MySQL.
- Data baru tidak ditulis ke CSV.
- Data CSV lama tetap tersedia.
- Data MySQL aktif masuk daftar publik.
- Data MySQL aktif masuk rekomendasi.
- Data MySQL nonaktif tidak masuk endpoint publik.
- Empat label kebutuhan tetap persis.
- API memakai Pydantic.
- Response JSON konsisten.
- Error ditangani dengan jelas.
- Artefak hilang atau rusak ditangani.
- Database gagal ditangani.
- Tidak ada scraping.
- Tidak ada dummy data sebagai sumber runtime utama.
- Tidak ada secret di source code.
- Test diperbarui.
- Aplikasi dapat dijalankan menggunakan:

  ```bash
  fastapi dev main.py
  ```

- File yang diubah dan hasil verifikasi dilaporkan secara ringkas.
