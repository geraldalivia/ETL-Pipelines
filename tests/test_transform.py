import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import (
    ubah_rating_ke_float,
    ubah_harga_ke_rupiah,
    ambil_angka_dari_warna,
    bersihkan_size_gender,
    hapus_data_kotor,
    hapus_duplikat,
    hapus_data_kosong,
    transform_data
)

@pytest.fixture
def data_sample():
    return [
        {
            "title": "Cullote Jeans",
            "price": "$119.50",
            "rating": "⭐ 3.0 / 5",
            "colors": "4 colors",
            "size": "Size: L",
            "gender": "Gender: Female",
            "timestamp": "2025-06-16"
        },
        {
            "title": "Produk Tidak Diketahui",
            "price": "Price Unavailable",
            "rating": "⭐ 4.0 / 5",
            "colors": "3 colors",
            "timestamp": "2025-06-16"
        },
        {
            "title": "Basic Comfort Shirt",
            "price": "$70.00",
            "rating": "⭐ 3.0 / 5",
            "colors": "5 colors",
            "size": "Size: L",
            "gender": "Gender: Female",
            "timestamp": "2025-06-16"
        },
        {
            "title": "Crop Millie Top",
            "price": "$20.00",
            "rating": "Not Rated",
            "colors": "4 colors",
            "size": None,
            "gender": None,
            "timestamp": "2025-06-16"
        },
        {
            "title": "Produk C",
            "price": "$30.00",
            "rating": "⭐ 4.8 / 5",
            "colors": "5 colors",
            "size": "Size: M",
            "gender": "Gender: Unisex",
            "timestamp": "2025-06-16"
        }
    ]

def test_rating_float(data_sample):
    hasil = ubah_rating_ke_float(data_sample.copy())
    assert isinstance(hasil[0]['rating'], float)
    assert hasil[0]['rating'] == 3.0

def test_harga_ke_rupiah(data_sample):
    hasil = ubah_harga_ke_rupiah(data_sample.copy(), kurs=15000)
    assert isinstance(hasil[0]['price'], float)
    assert round(hasil[0]['price'], 2) == 1792500.0  # 119.50 * 15000

def test_warna_jadi_angka(data_sample):
    hasil = ambil_angka_dari_warna(data_sample.copy())
    assert isinstance(hasil[0]['colors'], int)
    assert hasil[0]['colors'] == 4

def test_bersihkan_size_gender(data_sample):
    hasil = bersihkan_size_gender(data_sample.copy())
    assert hasil[0]['size'] == "L"
    assert hasil[0]['gender'] == "Female"

def test_hapus_kotoran(data_sample):
    hasil = hapus_data_kotor(data_sample.copy())
    # Harus menghapus 2 data: "Produk Tidak Diketahui" dan "Crop Millie Top"
    assert all(item['title'] != "Produk Tidak Diketahui" for item in hasil)
    assert all(item['rating'] != "Not Rated" for item in hasil)
    assert len(hasil) == 3

def test_hapus_duplikat(data_sample):
    data_bersih = hapus_data_kotor(data_sample.copy())
    hasil = hapus_duplikat(data_bersih)
    assert len(hasil) == 3  # Tidak ada data yang duplikat secara eksplisit

def test_hapus_kosong(data_sample):
    data_bersih = hapus_data_kotor(data_sample.copy())
    tanpa_duplikat = hapus_duplikat(data_bersih)
    hasil = hapus_data_kosong(tanpa_duplikat)
    assert all(all(val not in [None, ""] for val in item.values()) for item in hasil)
    assert len(hasil) == 3  # Semua data valid & lengkap

def test_transform_data(data_sample):
    hasil = transform_data(data_sample.copy())
    assert isinstance(hasil, list)
    assert len(hasil) == 3
    for item in hasil:
        assert isinstance(item['price'], float)
        assert isinstance(item['rating'], float)
        assert isinstance(item['colors'], int)
        assert isinstance(item['size'], str)
        assert isinstance(item['gender'], str)
