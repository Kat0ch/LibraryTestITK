from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from models import Author
from schemas import AuthorCreate, AuthorRead, AuthorUpdate
from database import SessionLocal

router = APIRouter(
    tags=["Authors"]
)


def get_db() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/authors/",
            response_model=List[AuthorRead],
            summary='Получить список авторов')
def read_authors(db: Session = Depends(get_db),
                 skip: int = Query(0, description="Количество пропусков при пагинации (смещение)"),
                 limit: int = Query(10, description="Максимальное количество авторов для отображения")):
    author = db.query(Author).offset(skip).limit(limit).all()
    return author


@router.get("/authors/{author_id}",
            response_model=AuthorRead,
            summary='Получить информацию об Авторе по ID')
def read_author(author_id: int = Path(description="ID автора"),
                db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/authors/",
             response_model=AuthorCreate,
             summary='Добавить Автора')
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.put("/authors/{author_id}",
            response_model=AuthorUpdate,
            summary='Обновить автора')
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author.name = author_update.name

    db.commit()
    db.refresh(author)
    return author


@router.delete("/authors/{author_id}",
               summary='Удалить автора по ID')
def delete_author(author_id: int = Path(description="ID автора"),
                  db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return author
