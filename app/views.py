from fastapi import APIRouter, UploadFile, File
from models import *

router = APIRouter()


@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}


@router.get('/data')
async def get_business_and_symptom_data(business_id: int = 1004, diagnostic: bool = True):
    try:
        return db_session\
            .query(BusinessData)\
            .filter(and_(BusinessData.business_id == business_id,
                     BusinessData.symptom_diagnostic == diagnostic))\
            .all()
    except Exception as e:
        return {'Error: ' + str(e)}

@router.post("/upload_business_csv/")
def upload_business_csv(file: UploadFile, file_format='utf-8'):
    try:
        load_business_data(get_csv_data(file.file, file_format))
        return {"Data loaded successfully."}

    except Exception as e:
        return {'Error: ' + str(e)}