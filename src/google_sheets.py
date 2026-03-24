"""
Integração com Google Sheets para exportar dados do DOU
"""

import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
import logging
import sys

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import *

logger = logging.getLogger(__name__)


class GoogleSheetsIntegration:
    """
    Classe para integrar com Google Sheets
    """
    
    def __init__(self):
        self.service = None
        self.spreadsheet_id = SPREADSHEET_ID
        self.sheet_name = SHEET_NAME
        self.authenticate()
    
    def authenticate(self):
        """
        Autentica com Google Sheets API
        """
        creds = None
        
        # Carrega token existente
        if os.path.exists(GOOGLE_TOKEN_FILE):
            with open(GOOGLE_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # Se não há credenciais válidas, faz login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Arquivo de credenciais não encontrado: {GOOGLE_CREDENTIALS_FILE}\n"
                        "Veja as instruções no README.md"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS_FILE, GOOGLE_SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salva as credenciais para próximas execuções
            with open(GOOGLE_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = discovery.build('sheets', 'v4', credentials=creds)
        logger.info("Autenticação com Google Sheets bem-sucedida")
    
    def create_spreadsheet(self, title: str = "DOU - IFMS") -> str:
        """
        Cria uma nova planilha no Google Sheets
        
        Args:
            title: Título da planilha
            
        Returns:
            ID da planilha criada
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [
                    {
                        'properties': {
                            'title': self.sheet_name
                        }
                    }
                ]
            }
            
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = result.get('spreadsheetId')
            logger.info(f"Planilha criada com sucesso: {spreadsheet_id}")
            return spreadsheet_id
            
        except Exception as e:
            logger.error(f"Erro ao criar planilha: {e}")
            raise
    
    def add_headers(self):
        """
        Adiciona headers à planilha
        """
        try:
            # Prepara os headers com formatação
            header_range = f"{self.sheet_name}!A1"
            values = [SHEET_COLUMNS]
            
            body = {
                'values': values
            }
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=header_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            # Formata os headers (negrito, background)
            self._format_headers()
            logger.info("Headers adicionados")
            
        except Exception as e:
            logger.error(f"Erro ao adicionar headers: {e}")
            raise
    
    def _format_headers(self):
        """
        Formata os headers com estilo
        """
        try:
            requests = [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 0.25,
                                    "green": 0.45,
                                    "blue": 0.66
                                },
                                "textFormat": {
                                    "bold": True,
                                    "foregroundColor": {
                                        "red": 1,
                                        "green": 1,
                                        "blue": 1
                                    }
                                },
                                "horizontalAlignment": "CENTER"
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                    }
                }
            ]
            
            body = {'requests': requests}
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
        except Exception as e:
            logger.debug(f"Aviso ao formatar headers: {e}")
    
    def append_rows(self, data: list):
        """
        Adiciona linhas de dados à planilha
        
        Args:
            data: Lista de dicionários com os dados
        """
        try:
            # Converte dicionários para listas na ordem correta das colunas
            rows = []
            for item in data:
                row = [
                    item.get('data_publicacao', ''),
                    item.get('titulo', ''),
                    item.get('secao', ''),
                    item.get('pagina', ''),
                    item.get('url', ''),
                    item.get('resumo', ''),
                    item.get('data_coleta', '')
                ]
                rows.append(row)
            
            # Determina o range para adicionar dados
            range_name = f"{self.sheet_name}!A2"
            
            body = {'values': rows}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            updated_rows = result.get('updates', {}).get('updatedRows', 0)
            logger.info(f"{updated_rows} linhas adicionadas à planilha")
            
        except Exception as e:
            logger.error(f"Erro ao adicionar dados: {e}")
            raise
    
    def get_spreadsheet_url(self) -> str:
        """
        Retorna a URL da planilha
        
        Returns:
            URL da planilha
        """
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
    
    def check_spreadsheet_exists(self) -> bool:
        """
        Verifica se a planilha existe
        
        Returns:
            True se existe, False caso contrário
        """
        try:
            self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            return True
        except:
            return False


if __name__ == "__main__":
    # Teste
    if SPREADSHEET_ID:
        sheets = GoogleSheetsIntegration()
        print(f"Conectado à planilha: {sheets.get_spreadsheet_url()}")
    else:
        print("SPREADSHEET_ID não configurado no config.py")
