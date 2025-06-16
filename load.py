from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# Buat fungsi untuk simpan ke Google Sheet
def simpan_ke_sheets(data, spreadsheet_id, sheet_name="Sheet1"):
    try:
        # Format data ke list of lists
        df = pd.DataFrame(data)
        nilai = [df.columns.tolist()] + df.values.tolist()

        # Setup kredensial Google
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file("service_account.json", scopes=scope)

        # Bangun service Google Sheets
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Clear isi sheet dulu biar gak numpuk
        sheet.values().clear(spreadsheetId=spreadsheet_id, range=sheet_name).execute()

        # Kirim data ke Google Sheets
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            valueInputOption="RAW",
            body={"values": nilai}
        ).execute()

        print(f"Data berhasil dikirim ke Google Sheets: {spreadsheet_id}")
    except Exception as e:
        print(f"Gagal simpan ke Google Sheets: {e}")
