from sqlmodel import create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///./foodstore.db"  # Cambia a tu motor preferido

engine = create_engine(DATABASE_URL, echo=True)

class SessionManager:
    def __init__(self):
        self.session = Session(engine)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

# Generador de sesión para dependencias de FastAPI
SessionLocal: Generator = SessionManager()