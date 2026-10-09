from fastapi import APIRouter, Request, HTTPException, status, Response

# add prefix and tags in app router when making key version rotation
router = APIRouter(prefix="/keys", tags=["key_lifecycle"])


@router.post(
    "/{key_id}/rotate",
    status_code=status.HTTP_200_OK,
)
async def rotate_key():
    return Response(status_code=status.HTTP_200_OK)


@router.post("/{key_id}/revoke", status_code=status.HTTP_200_OK)
async def revoke_key():
    return Response(status_code=status.HTTP_200_OK)
