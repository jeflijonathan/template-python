## Running the Application (Development)

To start the local FastAPI server with the auto-reload feature (the server automatically restarts every time a code change is made):

```bash
uvicorn main:app --reload
```

## 🛠️ System & Installation Requirements

If this is your first time downloading or moving this project to a new device, install all the required libraries with the following command:

```bash
pip install -r requirements.txt
```

## 🛠️ Code Quality & Linting (Ruff)

Proyek ini menggunakan **Ruff** sebagai alat penjamin kualitas kode (_linter_ dan _code formatter_). Ruff bertugas untuk memindai seluruh basis kode Python secara otomatis guna memastikan kode tetap bersih, konsisten, aman, dan bebas dari _bug_ pasif.

### 🚀 Mengapa Menggunakan Ruff?

- **Super Cepat:** Ditulis menggunakan bahasa Rust, Ruff mampu mengecek kode puluhan hingga ratusan kali lebih cepat dibandingkan _linter_ tradisional seperti Flake8, Black, atau Pylint.
- **All-in-One:** Menggantikan peran berbagai _tools_ sekaligus (menggantikan Flake8, isort, Black, bandit, dan banyak lagi).
- **Auto-Fix:** Mampu memperbaiki mayoritas kesalahan penulisan kode secara instan.

```bash
python -m ruff check .
```

```bash
pip install ruff
```

## Input libary

## 📦 Manajemen Dependensi (pipreqs)

Proyek ini menggunakan **pipreqs** untuk mengelola dan memperbarui file `requirements.txt`.

Berbeda dengan perintah `pip freeze` bawaan yang mencatat _seluruh_ package yang ada di dalam virtual environment (termasuk library _dependencies_ dari tools lain yang tidak sengaja terinstal), **pipreqs** bekerja secara pintar dengan hanya melihat kata kunci `import` yang benar-benar tertulis di dalam kode program Python Anda.

### 📊 Perbandingan: `pip freeze` vs `pipreqs`

| Fitur              | `pip freeze`                        | `pipreqs` (Proyek Ini)                         |
| :----------------- | :---------------------------------- | :--------------------------------------------- |
| **Cara Kerja**     | Mengosongkan isi venv ke dalam file | Memindai kode program (`import`)               |
| **Isi File**       | Kerap membengkak (_bloated_)        | Bersih dan esensial (_clean_)                  |
| **Efek ke Server** | Deployment lebih berat & lama       | Proses build kontainer/server jauh lebih cepat |

### 🚀 Mengapa Menggunakan pipreqs?

- **Clean & Minimalis:** File `requirements.txt` hanya berisi library utama yang benar-benar dijalankan oleh aplikasi.
- **Ukuran Aplikasi Ringan:** Mencegah pembengkakan ukuran _image container_ (Docker) atau memori server saat deployment karena tidak ada instalasi library sampah.
- **Pelacakan Versi Akurat:** Otomatis mendeteksi versi library yang sedang aktif digunakan di lokal komputer Anda untuk menghindari isu _production mismatch_.

---

### 💻 Panduan Penggunaan di Lokal

#### A. Bagi Developer (Update Dependensi Baru)

Jika Anda baru saja menambahkan atau menulis kode `import` baru dan ingin memperbarui daftar `requirements.txt`:

1. **Instalasi pipreqs** (Cukup lakukan sekali di awal)
   ```bash
   pip install pipreqs
   ```
2. **implement pipreqs**

```bash
python -m pipreqs.pipreqs . --force
```
