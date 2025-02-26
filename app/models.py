from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Example(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    example_column = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)


class BusinessTable(Base):
    __tablename__ = "business_symptom_data"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id = Column(Integer)
    business_name = Column(String(30), nullable=False)
    symptom_code = Column(String(15), nullable=False)
    symptom_name = Column(String(30), nullable=False)
    symptom_diagnostic = Column(String(30), nullable=False)