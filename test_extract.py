import sys
import os
import requests
import pytest
from bs4 import BeautifulSoup

# Tambahkan path agar bisa mengimpor modul dari folder utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import dan alias fungsi dari extract.py
from utils.extract import (
    ambil_konten_halaman as fetch_page_content,
    ambil_data_produk as extract_product_data,
    mulai_scraping as scrape_product_data
)

# HTML mock lengkap
@pytest.fixture
def html_lengkap():
    return '''
    <div class="product-details">
        <div class="product-title">Audrey White Top</div>
        <div class="price-container"><span class="price">$34.99</span></div>
        <p>Rating: 4.4</p>
        <p>1 Colors</p>
        <p>Size: L</p>
        <p>Gender: Women</p>
    </div>
    '''

# HTML mock kurang
@pytest.fixture
def html_kurang():
    return '''
    <div class="product-details">
        <div class="product-title">Basic skirt</div>
        <div class="price-container"><span class="price">$29.99</span></div>
        <p>Rating: 3.0</p>
    </div>
    '''

# HTML mock kosong
@pytest.fixture
def html_kosong():
    return '<div class="product-details"><p>no data</p></div>'


def test_fetch_page_content_success(monkeypatch):
    class FakeResponse:
        status_code = 200
        content = b"<html><body>ok</body></html>"

        def raise_for_status(self):
            pass

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    url = "https://contoh.com"
    result = fetch_page_content(url)
    assert result == b"<html><body>ok</body></html>"

def test_fetch_page_content_fail(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Something went wrong")

    monkeypatch.setattr(requests, "get", fake_get)

    url = "https://contoh.com"
    result = fetch_page_content(url)
    assert result is None

def test_extract_product_data_lengkap(html_lengkap):
    soup = BeautifulSoup(html_lengkap, 'html.parser')
    item = soup.find('div', class_='product-details')
    data = extract_product_data(item)

    assert data["title"] == "Audrey White Top"
    assert data["price"] == "$34.99"
    assert data["rating"] == "4.4"
    assert data["colors"] == "1 Colors"
    assert data["size"] == "Size: L"
    assert data["gender"] == "Gender: Women"
    assert "timestamp" in data

def test_extract_product_data_kurang(html_kurang):
    soup = BeautifulSoup(html_kurang, 'html.parser')
    item = soup.find('div', class_='product-details')
    data = extract_product_data(item)

    assert data["title"] == "Basic skirt"
    assert data["price"] == "$29.99"
    assert data["rating"] == "3.0"
    assert data["colors"] is None
    assert data["size"] is None
    assert data["gender"] is None

def test_extract_product_data_kosong(html_kosong):
    soup = BeautifulSoup(html_kosong, 'html.parser')
    item = soup.find('div', class_='product-details')
    result = extract_product_data(item)
    assert result is None

def test_scrape_product_data(monkeypatch):
    html = '''
    <div class="product-details">
        <div class="product-title">Trial produk</div>
        <div class="price-container"><span class="price">$12.50</span></div>
        <p>Rating: 4.0</p>
        <p>2 Colors</p>
        <p>Size: S</p>
        <p>Gender: Unisex</p>
    </div>
    '''

    class FakeResponse:
        status_code = 200
        content = html.encode("utf-8")

        def raise_for_status(self):
            pass

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result = scrape_product_data("https://fashion-studio.dicoding.dev", max_pages=2, jeda=0)
    assert isinstance(result, list)
    assert len(result) == 2  # karena max_pages=2
    assert result[0]["title"] == "Trial produk"
