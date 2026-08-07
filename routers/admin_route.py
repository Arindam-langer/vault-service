from fastapi import APIRouter, Request, HTTPException, status, Response

# add prefix and tags in app router when making key version rotation
router = APIRouter(prefix="/admin", tags=["ADMIN"])

token = "e964d4451303e6889f05456f619d9bd6b79dfdbd04a21b7a84bf59166f9cb4f2"


@router.post("/rotate")
def rotate_token(request: Request):
    try:
        vault_token = request.headers["X-Vault-Token"]
        if vault_token != token:
            Response(status_code=status.HTTP_404_NOT_FOUND, content="not found")

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden bitch"
        )
    return {"X-Vault-Token": vault_token}
