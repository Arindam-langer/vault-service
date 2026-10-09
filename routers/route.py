from fastapi import APIRouter, Request, HTTPException, status, Response

router = APIRouter()



@router.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

