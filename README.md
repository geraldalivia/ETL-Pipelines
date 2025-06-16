# ˚ ༘⋆🛍️｡˚ Fashion Product Scraper & ETL Pipeline

Proyek ini membangun pipeline Extract, Transform, Load (ETL) untuk mengambil data produk fashion dari situs e-commerce, membersihkannya, dan menyimpannya dalam format CSV. 

---

## 🔧 Teknologi

- Python 3.11
- BeautifulSoup
- Requests
- Pandas
- Pytest

---

## 📁 Struktur Projek

```
project-root/
├── tests/                   # Berisi unit tests untuk modul ETL
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── utils/                   # Berisi fungsi utama untuk extract, transform, dan load
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py                 # Pipeline utama yang menjalankan ETL end-to-end
├── requirements.txt        # Daftar dependensi Python
├── submission.txt          # File penjelasan projek ini
├── ETL-Pipeline.csv        # Hasil akhir produk yang disimpan ke file CSV
├── service_account.json    # Credential untuk Google Sheets API
├── README.md 
```

---

## 🚀 Cara Menjalankan

1. Clone repository ini dan masuk ke folder proyek. <br>
   `git clone https://github.com/geraldalivia/ETL-Pipelines.git` <br>
  ` cd ETL-Pipelines`<br>
   
3. Aktifkan virtual environment:
   ```bash
   source .env/bin/activate
   
4. Install dependency:  
   `pip install -r requirements.txt`

5. Jalankan pipeline ETL:  
   `python main.py`

6. Jalankan unit test:  
   `pytest tests/`

Catatan:
- Modul `extract.py` bertugas mengambil HTML dan mengekstrak data produk.
- Modul `transform.py` membersihkan data yang tidak lengkap.
- Modul `load.py` menyimpan hasil ke file CSV.

---

## 🔍 Isi file `ETL-Pipelines.csv`

| title       | price   | rating | colors | size | gender | timestamp           |
| ----------- | ------- | ------ | ------ | ---- | ------ | ------------------- |
| T-shirt 2   | 1634400 | 3,9    | 3      | M    | Women  | 2025-06-16 18:53:54 |
| Hoodie 3    | 7950080 | 4,8    | 3      | L    | Unisex | 2025-06-16 18:53:54 |
| Pants 4     | 7476960 | 3,3    | 3      | XL   | Men    | 2025-06-16 18:53:54 |
| Outerwear 5 | 5145440 | 3      | 3      | XXL  | Women  | 2025-06-16 18:53:54 |
| Jacket 6    | 2453920 | 3,3    | 3      | S    | Unisex | 2025-06-16 18:53:54 |
