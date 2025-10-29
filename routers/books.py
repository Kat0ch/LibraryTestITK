from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session, joinedload
from models import Book, Author
from schemas import BookCreate, BookRead, BookUpdate
from database import SessionLocal

router: APIRouter = APIRouter(
    tags=["Books"]
)


def get_db() -> None:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/books/",
            response_model=List[BookRead],
            summary='Получить список Книг')
def read_books(db: Session = Depends(get_db),
               author_id: Optional[int] = Query(None, description="Фильтрация по ID автора"),
               skip: int = Query(0, description="Количество пропусков при пагинации (смещение)"),
               limit: int = Query(10, description="Максимальное количество авторов для отображения")):
    query = db.query(Book).join(Book.author)
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)
    books = query.offset(skip).limit(limit).all()
    return [
        {
            "book_id": book.id,
            "title": book.title,
            "author_name": book.author.name
        }
        for book in books
    ]


@router.get("/books/{book_id}",
            response_model=BookRead,
            summary='Получить книгу по ID')
def read_book(book_id: int = Path(description="ID-книги"),
              db: Session = Depends(get_db)
              ):
    book = db.query(Book).join(Book.author).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "book_id": book.id,
        "title": book.title,
        "author_name": book.author.name
    }


@router.post("/books/",
             response_model=BookCreate,
             summary='Добавить книгу')
def create_book(book: BookCreate,
                db: Session = Depends(get_db)
                ):
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = Book(title=book.title, author_id=book.author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/books/{book_id}",
            response_model=BookUpdate,
            summary='Изменить книгу')
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_update.title
    book.author_id = book_update.author_id
    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}",
               summary='Удалить книгу по ID')
def delete_book(book_id: int = Path(description="ID-книги"),
                db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return book
