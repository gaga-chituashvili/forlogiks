from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Book Library API")

# --------- Book Models ---------

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: Optional[str] = None


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    genre: Optional[str] = None



books: List[Book] = []
current_id = 1


# --------- API Endpoints ---------

@app.post("/books", response_model=Book)
def add_book(book: BookCreate):
    global current_id

    new_book = Book(
        id=current_id,
        title=book.title,
        author=book.author,
        year=book.year,
        genre=book.genre
    )

    books.append(new_book)
    current_id += 1
    return new_book


@app.get("/books", response_model=List[Book])
def get_all_books():
    return books


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")
