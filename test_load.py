import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import simpan_ke_sheets

@pytest.fixture
def dummy_data():
    return [
        {
            "title": "Summer Pastel Floral Midi Dress",
            "price": 450000.0,
            "rating": 4.7,
            "colors": 4,
            "size": "L",
            "gender": "Unisex",
            "timestamp": "2025-06-16 12:00:00"
        }
    ]

@patch('utils.load.Credentials')
@patch('utils.load.build')
def test_simpan_ke_sheets(mock_build, mock_credentials, dummy_data):
    # Setup mocks
    mock_service = MagicMock()
    mock_sheet = MagicMock()
    mock_values = MagicMock()

    # Simulasikan .values().clear().execute() dan .values().update().execute()
    mock_sheet.spreadsheets.return_value.values.return_value.clear.return_value.execute.return_value = {}
    mock_sheet.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {}

    mock_build.return_value = mock_sheet

    # Jalankan fungsi yang diuji
    simpan_ke_sheets(dummy_data, spreadsheet_id="dummy_spreadsheet_id")

    # Pastikan semua fungsi dipanggil
    mock_credentials.from_service_account_file.assert_called_once_with(
        "service_account.json", scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.from_service_account_file.return_value)
    mock_sheet.spreadsheets.return_value.values.return_value.clear.assert_called()
    mock_sheet.spreadsheets.return_value.values.return_value.update.assert_called()
