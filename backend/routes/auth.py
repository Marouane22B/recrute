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


@auth_router.put("/plan/{user_id}/{plan_id}", status_code=status.HTTP_200_OK)
async def sign_in(user_id: int, plan_id: int):
    return await auth_controller.update_user_plan(user_id, plan_id)