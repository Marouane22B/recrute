from fastapi import APIRouter, status
from controllers.auth import AuthController
from shemas.auth import *

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"])

auth_controller = AuthController()


@auth_router.post("/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(params: SignUpParams):
    return await auth_controller.sign_up(params)

@auth_router.post("/sign-in", status_code=status.HTTP_200_OK)
async def sign_in(params: SignInParams):
    return await auth_controller.sign_in(params)