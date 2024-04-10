import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import SAMPLE_SPREADSHEET_ID, SHEET_NAME

CREDENTIALS_PATH = 'credentials.json'


def get_sheet():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        raise FileNotFoundError(f"Нет файла token.json, добавьте его в корень проекта для работы с Google sheets")
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         if os.path.exists(CREDENTIALS_PATH):
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 CREDENTIALS_PATH, SCOPES
    #             )
    #         else:
    #             return None
    #         creds = flow.run_local_server(port=0)
    #     with open("token.json", "w") as token:
    #         token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def write_data(data):
    sheet = get_sheet()
    if sheet is not None:
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SHEET_NAME,
        ).execute()
        values = result.get("values", [])
        first_empty_row = len(values) + 1 if values else 1
        sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A{first_empty_row}",
            valueInputOption="RAW",
            body={"values": data},
        ).execute()
    else:
        raise FileNotFoundError(f"Нет файла {CREDENTIALS_PATH}")

