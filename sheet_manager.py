import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetManager:
    def __init__(self, credentials_path, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Archivo de credenciales no encontrado en: {credentials_path}")
        
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def _get_first_sheet_name(self):
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        return sheets[0].get("properties", {}).get("title", "Sheet1")

    def ensure_headers(self):
        first_sheet_name = self._get_first_sheet_name()
        range_headers = f"'{first_sheet_name}'!A1:E1"
        
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range_headers).execute()
        values = result.get('values', [])
        
        headers = ["ID_Prenda", "Fecha_Venta", "Precio_Venta", "Coste_Estimado", "Beneficio"]
        
        if not values or values[0] != headers:
            body = {'values': [headers]}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_headers,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()

    def check_and_insert_sale(self, item_id, price, cost):
        # 1. Asegurar en caso de que no haya cabeceras
        self.ensure_headers()
        
        # 2. Leer la primera columna para buscar IDs
        first_sheet_name = self._get_first_sheet_name()
        range_id_col = f"'{first_sheet_name}'!A:A"
        
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=range_id_col).execute()
        values = result.get('values', [])
        
        existing_ids = [row[0] for row in values if row]
        
        if str(item_id) in existing_ids:
            return False, "El ID de esta URL ya está registrado en el inventario."
            
        # 3. Insertar nueva fila
        try:
            profit = float(price) - float(cost)
        except ValueError:
            return False, "Los precios deben ser numéricos."
            
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [str(item_id), date_str, str(price), str(cost), str(profit)]
        
        append_range = f"'{first_sheet_name}'!A:E"
        body = {
            'values': [new_row]
        }
        
        sheet.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=append_range,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        return True, "Registro insertado con éxito en la base de datos."
