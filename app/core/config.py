from typing import Optional

from pydantic import BaseSettings, EmailStr


RANGE = 'A1:E777'
SHEETS_VERSION = 'v4'
DRIVE_VERSION = 'v3'
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = {
    'properties': {'title': '', 'locale': 'ru_RU'},
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {'rowCount': 100, 'columnCount': 100}
        }
    }]
}
VALUE_INPUT_OPTION = 'USER_ENTERED'


class Settings(BaseSettings):
    app_title: str = 'Приложение QR-кот'
    description: str = 'Приложение для благотворительности'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
