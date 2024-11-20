import csv
import json
from io import StringIO
from uuid import uuid4

import reflex as rx

from catalog4_client.api_requests.openapijson import get_openapi_json
from catalog4_client.api_requests.vendors import add_vendors_batch, get_vendors
from catalog4_client.models import VendorBaseSchema, VendorBaseSchemaOut, VendorSchemaIn
from rxconfig import config


def show_vendor(vendor: VendorSchemaIn):
    return rx.table.row(
        # [rx.table.cell(name) for name, _ in vendor.get_fields.items()]
        rx.table.cell(vendor.id),
        rx.table.cell(vendor.name),
    )


class Vendors(rx.State):
    vendors: list[VendorBaseSchemaOut] = []
    current_vendor: VendorBaseSchemaOut = VendorBaseSchemaOut()
    clicked_data: str = 'Cell clicked: '
    clicked_cell: str = ''
    edited_cell: str = ''

    async def load_entries(self) -> list[VendorBaseSchemaOut] | None:
        status, data = await get_vendors()
        if status == 200 or status == 201:
            self.vendors: list[VendorBaseSchemaOut] = data

    @rx.event
    def get_clicked_data(self, pos):
        self.clicked_cell = f'Cell clicked: {pos}'

    @rx.event
    def get_edited_data(self, pos, val):
        col, row = pos
        self.vendors[row][self.columns[col]['id']] = val['data']
        # self.edited_cell = f'Cell edited: {pos}, Cell value: {val['data']}'

    columns = [
        {'title': 'ID', 'id': 'id', 'type': 'str', 'width': 0},
        {'title': 'Name', 'id': 'name', 'type': 'str', 'width': 500}
    ]


class VendorsToDB(rx.State):
    data: list[dict] = []
    current_vendor: VendorBaseSchemaOut = VendorBaseSchemaOut()
    clicked_data: str = 'Cell clicked: '
    clicked_cell: str = ''
    edited_cell: str = ''

    columns = [
        {'title': 'ID', 'id': 'id', 'type': 'str', 'width': 0},
        {'title': 'Name', 'id': 'name', 'type': 'str', 'width': 500}
    ]

    def add_row(self):
        empty_data = dict()
        for column in self.columns:
            empty_data[column['id']] = ''
        # self.data += empty_data
        self.data.append({'id': str(uuid4()), 'name': ''})

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_bytes = await file.read()
            buffer = StringIO(upload_bytes.decode('utf-8'))
            csv_reader = csv.DictReader(buffer)
            data = list(csv_reader)
            for item in data:
                item['id'] = str(uuid4())
            self.data = data

    @rx.event
    def get_edited_data(self, pos, val):
        col, row = pos
        self.data[row][self.columns[col]['id']] = val['data']
        # self.edited_cell = f'Cell edited: {pos}, Cell value: {val['data']}'

    async def handle_write_to_db(self):
        data_json = json.dumps(self.data)
        status, response_data = await add_vendors_batch(data_json=data_json)
        if status == 200:
            for item in self.data:
                if item not in response_data:
                    # TODO: what to do with error response rows?
                    ...


def editor():
    return rx.container(
        rx.box(
            rx.button(
                'Get vendors',
                on_click=Vendors.load_entries,
            )
        ),
        rx.data_editor(
            columns=Vendors.columns,
            data=Vendors.vendors,
            column_select='multi',
            max_column_auto_width=10000,
            column_auto_width=True,
            on_cell_clicked=Vendors.get_clicked_data,
            on_cell_edited=Vendors.get_edited_data,
        ),
        rx.hstack(
            rx.box(
                rx.button(
                    'Add row',
                    on_click=VendorsToDB.add_row,
                )
            ),
            rx.upload(
                rx.vstack(
                    rx.button(
                        'Upload csv'
                    ),
                ),
                id='upload2',
                multiple=False,
                accept={
                    'text/csv': ['.csv'],
                },
                disabled=False,
                # on_keyboard=True,
                on_drop=VendorsToDB.handle_upload(
                    rx.upload_files(upload_id='upload2')
                ),
                border='0px',
                padding='0px',
            ),
            rx.box(
                rx.button(
                    'Write to DB',
                    on_click=VendorsToDB.handle_write_to_db,
                )
            ),
        ),
        rx.data_editor(
            columns=VendorsToDB.columns,
            data=VendorsToDB.data,
            column_select='multi',
            max_column_auto_width=10000,
            column_auto_width=True,
            on_cell_edited=VendorsToDB.get_edited_data,
        ),
    )


app = rx.App()
app.add_page(editor, route='/vendors')
