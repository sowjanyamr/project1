import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("CREATE TABLE BOOKS ( ID SERIAL PRIMARY KEY,ISBN VARCHAR(15) NOT NULL,TITLE VARCHAR(255) NOT NULL,AUTHOR VARCHAR(255) NOT NULL,PUBLICATION_YEAR INTEGER NOT NULL)")

db.commit()
