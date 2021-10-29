import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe
from helpers import Helpers

scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/credentials.json', scopes)

client = gspread.authorize(creds)




def saveToGSheet(sheetName: str = 'New Spreadsheet'):
  sh = client.create(sheetName)
  ws = sh.sheet1
  set_with_dataframe(ws, Helpers.static_df)
  format_with_dataframe(ws, Helpers.static_df, include_column_header=True)
  sh.share(value=None, perm_type='anyone',  role='reader')
  print(sh.id)
  return f"https://docs.google.com/spreadsheets/d/{sh.id}"

#sh.share('mohamedxiv@gmail.com', perm_type='user', role='writer')
# sheet = client.open('ThisIsPublic').sheet1

# data = sheet.get_all_records()

#print(sh)