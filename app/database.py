from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Grab the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine (this is the connection to PostgreSQL)
engine = create_engine(DATABASE_URL)

# Each request gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our models will inherit from this
Base = declarative_base()

# This function gives us a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
 What Does Each Line Do?
```
create_engine()     → creates the actual connection to PostgreSQL
SessionLocal()      → a factory that creates database sessions
Base                → parent class all our table models will inherit
get_db()            → opens a session, gives it to a route, then closes it
```

Think of it like this:
```
engine        = the phone line to PostgreSQL
SessionLocal  = a phone call (one per request)
Base          = a template all tables are built from
get_db()      = picks up the phone, handles the call, hangs up

'''