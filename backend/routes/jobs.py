
from shemas.auth import *
from fastapi import APIRouter, status, UploadFile
from controllers.jobs import JobsController

jobs_router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

jobs_controller = JobsController()

@jobs_router.post("/jobs", status_code=status.HTTP_200_OK)
async def extract_from_cv(cv: UploadFile):
    """
    Extrait les informations d'un CV et génère une lettre de motivation.

    Args:
        cv (UploadFile): Le fichier de CV à traiter.

    Returns:
        dict: Contient le contenu du CV, les informations extraites et la lettre de motivation.
    """
    return await jobs_controller.extract_data_from_cv(cv)
