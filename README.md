# APRS-BOT-OIT-

Bot APRS yang terhubung ke jaringan APRS-IS dan dapat menerima serta membalas pesan sesuai perintah yang didefinisikan di folder `commands`. Bot ini dibuat dengan Python dan mendukung konfigurasi callsign, passcode, serta penambahan command module secara dinamis.

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

Semua file Python di folder `APRSBot-main/commands` akan dipindai secara otomatis oleh `main.py` pada saat aplikasi dijalankan. Jika file tersebut memiliki fungsi `handle_command`, maka modul tersebut akan dimuat dan dapat dipanggil saat pesan diterima.

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

## Lisensi

Repositori ini dibuat untuk keperluan proyek contoh dan pengembangan bot APRS pribadi. Silakan sesuaikan lisensinya sesuai kebutuhan Anda.

## Referensi

- APRS-IS server: `asia.aprs2.net`
- Library APRS: `aprslib`
- Bahasa pemrograman: Python

---

Kalau Anda mau, saya juga bisa bantu buatkan versi README yang lebih profesional untuk GitHub, termasuk badge, screenshot section, dan instruksi instalasi yang lebih rapi.
