from utils.extract import mulai_scraping
from utils.transform import transform_data
from utils.load import simpan_ke_sheets

def main():
    url = "https://fashion-studio.dicoding.dev/"
    sheet_id = "1gVYtJ9EgPrmWrwqVGUuOWifF9nTmNgIGSosILiD32f4"
    nama_sheet = "Sheet1"

    print("Mulai scraping data...")
    data = mulai_scraping(url)

    print(f"Data mentah terkumpul: {len(data)}")
    data_bersih = transform_data(data)
    print(f"Data setelah dibersihkan: {len(data_bersih)}")

    simpan_ke_sheets(data_bersih, spreadsheet_id=sheet_id, sheet_name=nama_sheet)

if __name__ == "__main__":
    main()