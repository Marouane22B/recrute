from shemas.auth import *
from utils.class_object import singleton

@singleton
class AuthController:
    def __init__(self) -> None:
        pass

    async def sign_up(self, params: SignUpParams):
        pass
    
    async def sign_in(self, params: SignInParams):
        pass
