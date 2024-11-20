from __future__ import annotations

from typing import List, Optional, Union
from uuid import UUID

import reflex as rx
from pydantic import BaseModel, Field
from reflex.base import Base

from catalog4_client.custom_types import ID_TYPE

# from schemas.models_base import ModelBaseSchema, ModelBaseSchemaOut


# class ModelBaseSchemaOut(rx.Model):
#     name: str = Field(..., title='Name')


class VendorBaseSchemaOut(rx.Model):
    name: str = Field(..., title='Name')
    id: UUID = Field(..., title='Id')


# class ModelSchemaOut(rx.Model, table=True):
#     id: UUID = Field(..., title='Id')
#     name: str = Field(..., title='Name')
#     vendor: Optional[VendorBaseSchemaOut]
#     is_original: Optional[bool] = Field(False, title='Is Original')
#     alternatives: Optional[List[ModelBaseSchemaOut]
#                            ] = Field(None, title='Alternatives')


class VendorBaseSchema(rx.Model, table=True):
    name: str = Field(..., title='Name')


class VendorSchemaIn(VendorBaseSchema):
    id: UUID = Field(..., title='Id')
