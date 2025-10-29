from typing import Optional
from pydantic import BaseModel


# Base
class AuthorBase(BaseModel):
    name: str


class BookBase(BaseModel):
    title: str
    author_id: int


# Create
class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    pass


# Update
class AuthorUpdate(AuthorBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str]
    author_id: Optional[int]


# Read
class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookRead(BaseModel):
    book_id: int
    title: str
    author_name: str

    class Config:
        from_attributes = True
