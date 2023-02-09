from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import (settings, RANGE, SHEETS_VERSION,
                             DRIVE_VERSION, FORMAT, SPREADSHEET_BODY,
                             VALUE_INPUT_OPTION)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    SPREADSHEET_BODY['properties']['title'] = now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        row = [str(project.name), str(project.close_date - project.create_date),
               str(project.description)]
        table_values.append(row)
    head = table_values[0:3]
    sorted_data = sorted(table_values[3:], key=lambda project: project[1])
    result = head + sorted_data
    update_body = {
        'majorDimension': 'ROWS',
        'values': result
    }
    response = await wrapper_services.as_service_account( # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
