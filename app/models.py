from sqlalchemy import Column, Integer, String, DateTime, create_engine, and_, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import csv
import codecs
import settings

Base = declarative_base()

class Example(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    example_column = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)

class DiagnosisData(Base):
    __tablename__ = "diagnosis"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    symptom_id = Column(String(16), nullable=False)
    symptom_name = Column(String(100), nullable=True)
    patient_name = Column(String(100), nullable=False)
    patient_id = Column(Integer, nullable=False)
    diagnosis = Column(Boolean, nullable=False)


class BusinessData(Base):
    """
    business and symptom data

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
    symptom_diagnostic_raw = Column(String(30), nullable=True)
    symptom_diagnostic = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"BusinessData(id={self.id!r}, " \
               f"business_id={self.business_id!r}, " \
               f"business_name={self.business_name!r}, " \
               f"symptom_code={self.symptom_code!r}, " \
               f"symptom_name={self.symptom_name!r}, " \
               f"symptom_diagnostic_raw={self.symptom_diagnostic_raw!r}, " \
               f"symptom_diagnostic={self.symptom_diagnostic!r})"



# create engine and session
engine = create_engine(settings.DB_URL)
session = sessionmaker()
session.configure(bind=engine)
db_session = session()

# create the table and load data from the business symptom data csv
Base.metadata.create_all(engine)

def get_csv_data(file, format='utf-8'):
    """
    Returns a list(dict) of rows and their values
    :param file: A file-like object
    :param format: The format that file is in
    :return: the contained data in a list(dict)
    """
    data = []
    csv_reader = csv.DictReader(codecs.iterdecode(file, format))
    for row in csv_reader:
        data.append(row)
    return data

def str_is_true(s: str):
    s_clean = s.replace(" ", "").lower()
    return s_clean == "true" or s_clean == "yes" or s_clean == "bad" or s_clean == "positive"

def str_is_false(s: str):
    s_clean = s.replace(" ", "").lower()
    return s_clean == "false" or s_clean == "no" or s_clean == "good" or s_clean == "negative"

def str_to_bool(s: str):
    if str_is_true(s):
        return True
    elif str_is_false(s):
        return False
    raise ValueError(f"Given string {s} does not contain a recognized boolean!")

def str_is_bool(s: str):
    try:
        str_to_bool(s)
        return True
    except ValueError:
        return False

def load_business_data(data):
    """
    Loads data into the business symptom database
    Allows for duplicate data, but distinguishes entries by id
    :param data: list of dicts for data to be loaded
    """
    exception_strs = []
    for obj in data:

        error_info = []
        for field in ('Business ID', 'Business Name', 'Symptom Code', 'Symptom Name'):
            if obj[field] == '':
                error_info.append(f"does not contain {field}")

        if 'Symptom Diagnostic' in obj.keys() and not str_is_bool(obj['Symptom Diagnostic']):
            error_info.append(f"\"{obj['Symptom Diagnostic']}\" not recognized as a true/false value")

        if len(error_info) != 0:
            exception_strs.append(f"Row with data {obj} given, " + ", ".join(error_info))
            continue

        try:
            business_data = BusinessData(**{
                'business_id' : obj['Business ID'],
                'business_name' : obj['Business Name'],
                'symptom_code' : obj['Symptom Code'],
                'symptom_name' : obj['Symptom Name'],
                'symptom_diagnostic_raw' : obj['Symptom Diagnostic'],
                'symptom_diagnostic' : str_to_bool(obj['Symptom Diagnostic'])
            })
            db_session.add(business_data)
            db_session.commit()
        except:
            db_session.rollback()
            raise Exception("Failed to add entry to database.")


    if len(exception_strs) != 0:
        raise ValueError("Errors in data submission.  " + "  ".join(exception_strs))