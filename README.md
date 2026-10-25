# APRS-BOT-OIT-

Bot APRS yang terhubung ke jaringan APRS-IS dan dapat menerima serta membalas pesan sesuai perintah yang didefinisikan di folder `commands`. Bot ini dibuat dengan Python dan mendukung konfigurasi callsign, passcode, serta fitur tambahan seperti upload gambar ke GitHub.

## Fitur

- Terhubung ke server APRS-IS (`asia.aprs2.net:14580`)
- Menerima pesan yang ditujukan ke callsign bot
- Mengirim ACK otomatis untuk paket yang masuk
- Memuat command secara dinamis dari folder `commands`
- Mendukung perintah seperti `ping`, `help`, `time`, dan `commands`
- Dapat dikembangkan dengan menambahkan file Python baru di folder `commands`
- Mendukung pembuatan gambar selamat datang yang di-upload ke GitHub untuk pesan `ping`

## Struktur Proyek

```text
APRS-BOT-OIT-
├── README.md
├── APRSBot-main/
│   ├── main.py
│   └── commands/
│       ├── commands.py
│       ├── help.py
│       ├── ping.py
│       ├── time.py
│       └── modules/
│           └── assets/
└── .gitignore
```

## Prasyarat

Pastikan perangkat Anda sudah memiliki:

- Python 3.x
- Paket Python berikut:

```bash
pip install aprslib pillow requests
```

## Konfigurasi

Buka file `APRSBot-main/main.py` lalu sesuaikan pengaturan berikut:

```python
CALLSIGN = "YD3ADB-7"
PASSCODE = "23973"
SERVER = "asia.aprs2.net"
PORT = 14580
```

- `CALLSIGN`: callsign APRS bot Anda
- `PASSCODE`: passcode APRS untuk callsign tersebut
- `SERVER` dan `PORT`: server APRS-IS yang digunakan

> Pastikan callsign dan passcode yang digunakan valid sebelum menjalankan bot.

## Cara Mendapatkan GitHub Token (untuk fitur `ping`)

Fitur `ping` dapat membuat gambar selamat datang lalu mengunggahnya ke repositori GitHub. Untuk itu, Anda perlu membuat token GitHub dan menyimpannya di environment variable.

### 1) Buat repository GitHub

Jika Anda ingin hasil upload gambar disimpan di repo GitHub, pastikan repo sudah dibuat terlebih dahulu.

Contoh:

```text
https://github.com/<username>/<repository>
```

### 2) Membuat Personal Access Token (PAT)

Cara umum:

1. Buka GitHub
2. Klik avatar di kanan atas → `Settings`
3. Masuk ke `Developer settings`
4. Pilih `Personal access tokens`
5. Klik `Fine-grained tokens` (disarankan) atau `Classic`
6. Klik `Generate new token`
7. Atur permission minimal:
   - `Repository permissions` → `Contents` → `Read and write`
8. Pilih repo yang akan digunakan
9. Copy token yang muncul
10. Simpan token tersebut dengan aman, karena token hanya tampil sekali

> Jangan membagikan token ke publik atau ke repo lain.

### 3) Menyimpan token di environment variable

Pada Linux/macOS:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Pada Windows PowerShell:

```powershell
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Pada Windows CMD:

```cmd
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Untuk penggunaan permanen:

```powershell
setx GITHUB_TOKEN "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4) Atur repo tujuan di file `ping.py`

Buka file:

```python
APRSBot-main/commands/ping.py
```

Lalu sesuaikan bagian ini:

```python
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "keitopriss/u"
GITHUB_BRANCH = "main"
```

Ubah ke repositori Anda sendiri, misalnya:

```python
GITHUB_REPO = "username/nama-repo-anda"
GITHUB_BRANCH = "main"
```

> Jika repo bersifat privat, token harus memiliki akses ke repo tersebut.

### 5) Jika tidak ingin menggunakan upload GitHub

Jika Anda tidak membutuhkan fitur upload gambar, Anda dapat:

- menghapus atau menonaktifkan bagian upload pada `ping.py`, atau
- tetap membiarkan `GITHUB_TOKEN` kosong agar fungsi `ping` akan menampilkan pesan default tanpa gambar

## Menjalankan Bot

1. Masuk ke folder proyek:

```bash
cd APRSBot-main
```

2. Jalankan bot:

```bash
python main.py
```

Bot akan melakukan koneksi ke APRS-IS, menunggu pesan masuk, dan otomatis memproses perintah yang dikirim ke callsignnya.

## Cara Kerja Command

Semua file Python di folder `APRSBot-main/commands` akan dipindai secara otomatis oleh `main.py` pada saat aplikasi dijalankan. Jika file tersebut memiliki fungsi `handle_command`, maka modul tersebut akan di-load otomatis dan siap dipanggil melalui callsign bot.

Contoh command yang tersedia:

- `help` → menampilkan sumber repo
- `commands` → menampilkan daftar command yang tersedia
- `ping` → mengirim ucapan selamat datang serta gambar
- `time` → menampilkan waktu

## Menambahkan Command Baru

Buat file baru di folder `APRSBot-main/commands`, misalnya:

```python
# APRSBot-main/commands/hello.py

def handle_command():
    return "Halo! Ini adalah command baru."
```

Maka bot akan otomatis mengenali command `hello` saat dikirim ke bot.

## Catatan Penting

- File `ping.py` memerlukan environment variable `GITHUB_TOKEN` untuk mengunggah gambar ke repositori GitHub.
- Jika Anda tidak membutuhkan fitur upload gambar, Anda dapat menyesuaikan atau menghapus bagian tersebut.
- Untuk produksi, disarankan untuk menyimpan konfigurasi sensitif seperti `CALLSIGN` dan `PASSCODE` di environment variable atau file konfigurasi yang aman.
- Pastikan repository yang dituju benar, karena token GitHub hanya bekerja pada repo yang memiliki izin akses yang sesuai.
- Untuk menghindari batasan panjang URL APRS, link hasil upload gambar harus tetap singkat. `ping.py` sudah mencoba memeriksa panjang link-nya.

## Troubleshooting Umum

### Error: `GITHUB_TOKEN belum diisi di terminal`

Artinya token belum di-set di environment variable. Pastikan Anda menjalankan perintah `export` atau `set` sebelum menyalakan bot.

### Error 403 / permission denied saat upload

- Token belum memiliki izin `Contents: Read and write`
- Repo yang dituju tidak sesuai
- Repo bersifat privat tetapi token tidak memiliki akses

### Bot tidak menerima pesan

- Pastikan `CALLSIGN` dan `PASSCODE` valid
- Pastikan port dan server benar
- Cek koneksi internet dan akses ke APRS-IS

## Lisensi

Repositori ini dibuat untuk keperluan proyek contoh dan pengembangan bot APRS pribadi. Silakan sesuaikan lisensinya sesuai kebutuhan Anda.

## Referensi

- APRS-IS server: `asia.aprs2.net`
- Library APRS: `aprslib`
- Bahasa pemrograman: Python
- GitHub Token Docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

---

Kalau Anda mau, saya juga bisa bantu buatkan versi README yang lebih profesional untuk GitHub, termasuk badge, screenshot section, dan instruksi instalasi yang lebih rapi.
