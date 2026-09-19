from fastapi import APIRouter

router = APIRouter(prefix='/health', tags=['health'])


@router.get('')
def health() -> dict[str, str]:
    return {'status': 'ok', 'service': 'darukaa-earth-backend'}


@router.get('/db')
def database_health() -> dict[str, str]:
    return {'status': 'ok', 'database': 'pending-setup'}
