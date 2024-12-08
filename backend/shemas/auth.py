from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic import field_validator, model_validator

# Sign Up Params
class SignUpParams(BaseModel):
    pass
    
# Sign In Params
class SignInParams(BaseModel):
    email: EmailStr
    password: str