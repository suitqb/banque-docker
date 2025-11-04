from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

from db import Base

class Compte(Base):
    __tablename__ = "comptes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    solde = Column(Numeric(12, 2), nullable=False, default=0)
