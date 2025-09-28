from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class AuthorInput(BaseModel):
    first_name: str = ""
    last_name: str = ""
    bio: str = ""


class CoverInput(BaseModel):
    cover_image: Optional[str] = ""


class BookDetails(BaseModel):
    isbn: str = Field(alias="ISBN")
    year: Optional[str] = Field(alias="Год", default=None)
    pages: int = Field(default=0, alias="Страниц")

    class Config:
        populate_by_name = True


class BookInput(BaseModel):
    book_title: str
    description: str
    author: List[AuthorInput]
    cover: CoverInput
    details: BookDetails
    url: Optional[str] = None
    price: Optional[dict] = None

    @field_validator("details")
    @classmethod
    def ensure_isbn(cls, v: BookDetails) -> BookDetails:
        if not v.isbn.strip():
            raise ValueError("ISBN is required")
        return v

    class Config:
        populate_by_name = True
