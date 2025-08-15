from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional


class AuthorInput(BaseModel):
    first_name: str = ""
    last_name: str = ""
    bio: str = ""


class CoverInput(BaseModel):
    cover_image: Optional[str] = ""


class BookDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    isbn: str = Field(alias="ISBN")
    year: Optional[str] = Field(alias="Год", default=None)
    pages: int = Field(default=0, alias="Страниц")


class BookInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    book_title: str
    description: str
    author: List[AuthorInput]
    cover: CoverInput
    details: BookDetails

    @field_validator("details")
    @classmethod
    def ensure_isbn(cls, v: BookDetails) -> BookDetails:
        if not v.isbn.strip():
            raise ValueError("ISBN is required")
        return v
