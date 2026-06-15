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

## 📦 Manajemen Dependensi (pipreqs)

This project uses **pipreqs** to manage and update the `requirements.txt` file.

Unlike the default `pip freeze` command, which lists all packages in the virtual environment (including library dependencies from accidentally installed tools), **pipreqs** intelligently looks only at the `import` keywords actually written in your Python code.

### 📊 Comparison: `pip freeze` vs `pipreqs`

| Features           | `pip freeze`                       | `pipreqs` (This Project)                   |
| :----------------- | :--------------------------------- | :----------------------------------------- |
| **How ​​It Works** | Emptying venv contents into a file | Scanning program code (`import`)           |
| **File Contents**  | Often bloated                      | Clean and essential                        |
| **Server Impact**  | Heavier & slower deployment        | Much faster container/server build process |

### 🚀 Why Use pipreqs?

- **Clean & Minimalist:** The `requirements.txt` file only contains the core libraries that are actually used by the application.
- **Lightweight Application Size:** Prevents bloating of container (Docker) image size or server memory during deployment because there are no unnecessary library installations.
- **Accurate Version Tracking:** Automatically detects the currently active library version on your local machine to avoid production mismatch issues.

---

### 💻 Local Usage Guide

#### A. For Developers (Updating New Dependencies)

If you've recently added or written new `import` code and want to update your `requirements.txt` list:

1. **Install pipreqs** (Just do it once at the start)

```bash
pip install pipreqs
```

2. **implement pipreqs**

```bash
python -m pipreqs.pipreqs . --force
```
