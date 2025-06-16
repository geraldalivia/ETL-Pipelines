import re

def ubah_rating_ke_float(data):
    for item in data:
        try:
            if isinstance(item['rating'], str):
                angka = re.sub(r'[⭐\s/5]', '', item['rating']).strip()
                item['rating'] = float(angka)
        except:
            item['rating'] = None
    return data

def ubah_harga_ke_rupiah(data, kurs=16000):
    for item in data:
        try:
            if isinstance(item['price'], str) and "$" in item['price']:
                dollar = float(item['price'].replace('$', '').strip())
                item['price'] = float(dollar * kurs)
        except:
            item['price'] = None
    return data

def ambil_angka_dari_warna(data):
    for item in data:
        try:
            if isinstance(item['colors'], str):
                hasil = re.search(r'\d+', item['colors'])
                item['colors'] = int(hasil.group()) if hasil else None
        except:
            item['colors'] = None
    return data

def bersihkan_size_gender(data):
    for item in data:
        try:
            if isinstance(item['size'], str):
                item['size'] = item['size'].replace("Size:", "").strip()
            if isinstance(item['gender'], str):
                item['gender'] = item['gender'].replace("Gender:", "").strip()
        except:
            pass
    return data

def hapus_data_kotor(data):
    data_bersih = []
    for item in data:
        if item.get('title') == "Unknown Product":
            continue
        if item.get('rating') in ["Invalid Rating / 5", "Not Rated"]:
            continue
        if item.get('price') in ["Price Unavailable", None]:
            continue
        data_bersih.append(item)
    return data_bersih

def hapus_data_kosong(data):
    return [item for item in data if all(v not in [None, ""] for v in item.values())]

def hapus_duplikat(data):
    unik = []
    sudah = set()
    for item in data:
        kunci = (item['title'], item['price'], item['rating'])
        if kunci not in sudah:
            sudah.add(kunci)
            unik.append(item)
    return unik

def transform_data(data):
    try:
        data = hapus_data_kotor(data)
        data = hapus_data_kosong(data)
        data = hapus_duplikat(data)
        data = ubah_harga_ke_rupiah(data)
        data = ubah_rating_ke_float(data)
        data = ambil_angka_dari_warna(data)
        data = bersihkan_size_gender(data)
        data = hapus_data_kosong(data)
    except Exception as e:
        print("Error saat transformasi:", e)
    return data
