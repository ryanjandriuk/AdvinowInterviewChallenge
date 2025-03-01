from sqlalchemy import Column, Integer, String, DateTime, create_engine, and_, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import csv
import util

Base = declarative_base()

class Example(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    example_column = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)


class BusinessData(Base):
    """
    static class for business and symptom data

    Attributes:
        __tablename__           Name of the table, always "business_symptom_data"
        id                      An sqlalchemy Column(Integer) for a unique identifier for the row entry
        business_id             An sqlalchemy Column(Integer) for the id of the business
        business_name           An sqlalchemy Column(String(30)) for the name of the business
        symptom_code            An sqlalchemy Column(String(15)) for the code of the symptom of the entry
        symptom_name            An sqlalchemy Column(String(30)) for the name of the symptom of the entry
        symptom_diagnostic_raw  An sqlalchemy Column(String(30)) for the raw string diagnosis of the symptom of the entry
        symptom_diagnostic      An sqlalchemy Column(Boolean) for the converted diagnosis of the symptom of the entry
    """
    __tablename__ = "business_symptom_data"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id = Column(Integer)
    business_name = Column(String(30), nullable=False)
    symptom_code = Column(String(15), nullable=False)
    symptom_name = Column(String(30), nullable=False)
    symptom_diagnostic_raw = Column(String(30), nullable=False)
    symptom_diagnostic = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"BusinessData(id={self.id!r}, " \
               f"business_id={self.business_id!r}, " \
               f"business_name={self.business_name!r}, " \
               f"symptom_code={self.symptom_code!r}, " \
               f"symptom_name={self.symptom_name!r}, " \
               f"symptom_diagnostic_raw={self.symptom_diagnostic_raw!r}, " \
               f"symptom_diagnostic={self.symptom_diagnostic!r})"



# create engine and session
engine = create_engine('sqlite:///storage.db')
session = sessionmaker()
session.configure(bind=engine)
db_session = session()

# create the table and load data from the business symptom data csv
Base.metadata.create_all(engine)
def GetCSVData(file_name: str):
    data = []
    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            data.append(row)
    return data

try:
    data = GetCSVData("data/business_symptom_data.csv")
    for obj in data:
        business_data = BusinessData(**{
            'business_id' : obj['Business ID'],
            'business_name' : obj['Business Name'],
            'symptom_code' : obj['Symptom Code'],
            'symptom_name' : obj['Symptom Name'],
            'symptom_diagnostic_raw' : obj['Symptom Diagnostic'],
            'symptom_diagnostic' : util.str_to_bool(obj['Symptom Diagnostic'])
        })
        db_session.add(business_data)
    db_session.commit()
except:
    db_session.rollback()
    print("Failed to initialize business symptom database")