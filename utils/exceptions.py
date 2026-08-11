from fastapi import HTTPException, status

"""
Centralised HTTP exception helpers.

Instead of raising HTTPException directly in service layers,
all error responses are defined here so status codes and
messages stay consistent across the entire API.

"""

def raise_not_found(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def raise_unauthorized(detail: str = "Incorrect password"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def raise_conflict(detail: str):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def raise_bad_request(detail: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)