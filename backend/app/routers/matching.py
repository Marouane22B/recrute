# Routes pour la gestion des correspondances (matching)
from fastapi import APIRouter

router = APIRouter()

@router.get("/matching")
async def get_matching():
    return {"message": "Matching system route"}
