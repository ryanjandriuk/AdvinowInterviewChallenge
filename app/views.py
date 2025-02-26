from fastapi import APIRouter

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
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
