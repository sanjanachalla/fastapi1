from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None

# sample data
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
]

# get all books
@app.get("/books", response_model=List[Book])
async def get_books():
    return [Book(**b) for b in books]

# get one book using id
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return Book(**b)
    raise HTTPException(status_code=404, detail="book not found")

# add a new book
@app.post("/books", response_model=Book)
async def add_book(book: Book):
    for b in books:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail="id already exists")
    books.append(book.dict())
    return book

# update book
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    for i in range(len(books)):
        if books[i]["id"] == book_id:
            books[i] = book.dict()
            return book
    raise HTTPException(status_code=404, detail="book not found")

# delete book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i]["id"] == book_id:
            books.pop(i)
            return {"msg": "deleted"}
    raise HTTPException(status_code=404, detail="book not found")

# search book using query params
@app.get("/search", response_model=List[Book])
async def search_books(author: Optional[str] = None, year: Optional[int] = None):
    result = books
    if author:
        result = [b for b in result if b["author"] == author]
    if year:
        result = [b for b in result if b["year"] == year]
    return [Book(**b) for b in result]
