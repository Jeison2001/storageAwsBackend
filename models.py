from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileRecord(Base):
    __tablename__ = 'FileRecord'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    url = Column(String)

    def __init__(self, descripcion, url):
        self.descripcion = descripcion
        self.url = url
