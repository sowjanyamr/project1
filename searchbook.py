import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#books=db.execute("SELECT * FROM BOOKS WHERE PUBLICATION_YEAR = :year",{"year":1973}).fetchall()
try:
    books = db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn AND TITLE LIKE :title",{"isbn":"1857231082","title":"%%The Black%%" })
    #books = db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn AND TITLE LIKE '%title%'",{"isbn":1857231082,"title":The Black})
    #print(f"title {books}")
    for book in books:
        print(f"title {book.title}")
        print(f"id is {book.id}, title::{book.title},written by {book.author},published in the year {book.publication_year}")
except ValueError:
    print(f"error")

db.commit()
