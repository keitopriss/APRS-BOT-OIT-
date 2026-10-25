import os
import uuid
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_IMAGE = os.path.join(BASE_DIR, "modules", "assets", "selamat_datang_aprs.jpg")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "keitopriss/u"
GITHUB_BRANCH = "main"

UPLOAD_TIMEOUT = 15  # detik


def upload_github(path):
    """Upload gambar ke repo GitHub publik, kembalikan link raw-nya."""
    if not GITHUB_TOKEN:
        raise Exception("GITHUB_TOKEN belum diisi di terminal")
    nama = datetime.now().strftime("%d%H%M%S") + uuid.uuid4().hex[:1] + ".jpg"
    with open(path, "rb") as f:
        konten = base64.b64encode(f.read()).decode()
    resp = requests.put(
        f"https://api.github.com/repos/{GITHUB_REPO}/contents/{nama}",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        json={"message": f"welcome {nama}", "content": konten, "branch": GITHUB_BRANCH},
        timeout=UPLOAD_TIMEOUT,
    )
    resp.raise_for_status()
    link = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{nama}"
    if len(link) > 67:
        print(f"[ping] PERINGATAN: link {len(link)} karakter, melebihi batas APRS 67")
    return link


def draw_centered_text(draw, img_width, y, text, font, fill="white", outline="black"):
    """Gambar satu baris teks rata tengah dengan outline."""
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (img_width - (bbox[2] - bbox[0])) / 2
    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def generate_and_upload(name):
    """Buat gambar berisi nama + waktu panggilan, upload, kembalikan link."""
    img = Image.open(BASE_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)

    line1 = f"Selamat Datang, {name}!"
    line2 = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    try:
        font1 = ImageFont.truetype("arial.ttf", max(28, int(img.width / 18)))
        font2 = ImageFont.truetype("arial.ttf", max(18, int(img.width / 30)))
    except Exception:
        font1 = font2 = ImageFont.load_default()

    b1 = draw.textbbox((0, 0), line1, font=font1)
    b2 = draw.textbbox((0, 0), line2, font=font2)
    h1, h2 = b1[3] - b1[1], b2[3] - b2[1]

    spacing = 10
    y1 = img.height - (h1 + spacing + h2) - int(img.height * 0.06)
    y2 = y1 + h1 + spacing

    draw_centered_text(draw, img.width, y1, line1, font1)
    draw_centered_text(draw, img.width, y2, line2, font2)

    out_path = os.path.join(
        BASE_DIR, "modules", "assets", f"welcome_{name}_{uuid.uuid4().hex[:8]}.jpg"
    )
    img.save(out_path, quality=85)
    try:
        return upload_github(out_path)
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)


def handle_command(from_call=None):
    """Balas dengan ucapan + link gambar selamat datang berisi nama callsign dan waktu."""
    name = from_call or "APRS"
    try:
        link = generate_and_upload(name)
        jam = datetime.now().strftime("%H:%M:%S")
        return f"Selamat datang di APRSBOT UKDC, {name}! {jam} {link}"
    except Exception as e:
        print(f"[ping] gagal membuat gambar: {e}")
        return f"Selamat datang di APRSBOT UKDC, {name}! (gambar belum tersedia)"