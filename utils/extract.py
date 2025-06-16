# extract.py
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Header untuk akses halaman
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Ambil isi HTML dari halaman
def ambil_konten_halaman(url):
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.content
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil halaman: {url}, error: {e}")
        return None

# Ekstrak data dari satu produk
def ambil_data_produk(section):
    try:
        title = section.find(class_="product-title").text.strip()

        price_tag = section.find("div", class_="price-container")
        if price_tag:
            price_text = price_tag.find(class_="price")
        else:
            price_text = section.find("p", class_="price")
        price = price_text.text.strip() if price_text else None

        detail_tags = section.find_all("p")

        rating = next((p.text.replace("Rating:", "").strip() for p in detail_tags if "Rating:" in p.text), None)
        colors = next((p.text.strip() for p in detail_tags if "Color" in p.text), None)
        size = next((p.text.strip() for p in detail_tags if "Size:" in p.text), None)
        gender = next((p.text.strip() for p in detail_tags if "Gender:" in p.text), None)

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
            "timestamp": waktu
        }

    except Exception as e:
        print(f"Error saat ekstraksi produk: {e}")
        return None

# Loop semua halaman untuk scraping
def mulai_scraping(url, max_pages=50, jeda=2):
    hasil = []

    for halaman in range(1, max_pages + 1):
        if halaman == 1:
            full_url = url
        else:
            full_url = f"{url}page{halaman}"
        
        print(f"Scraping halaman ke-{halaman}: {full_url}")

        konten = ambil_konten_halaman(full_url)
        if not konten:
            break

        soup = BeautifulSoup(konten, "html.parser")
        semua_produk = soup.find_all("div", class_="product-details")

        if not semua_produk:
            print("Tidak ada produk lagi ditemukan.")
            break

        for produk in semua_produk:
            data = ambil_data_produk(produk)
            if data:
                hasil.append(data)

        time.sleep(jeda)

    return hasil
