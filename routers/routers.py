from fastapi import APIRouter, Depends, status, Response
from db.database import get_session
from db.crud import Session
from models.models import PII_data
from services.service import (
    create_token_service,
    get_token_service,
    revoke_token_service,
)

# add prefix and tags in app router when making key version rotation
router = APIRouter()


@router.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/vault",
    status_code=status.HTTP_201_CREATED,
)
async def create_token(
    pii_data: PII_data,
    session: Session = Depends(get_session),
):
    return create_token_service(session=session, pii_data=pii_data)


@router.get("/vault/{token_id}")
async def get_token(
    token_id: str,
    session: Session = Depends(get_session),
):
    return get_token_service(session=session, token_id=token_id)


@router.delete("/vault/{token_id}")
async def delete_token(token_id: str, session: Session = Depends(get_session)):
    return revoke_token_service(session=session, token_id=token_id)
