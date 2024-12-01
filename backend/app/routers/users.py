from fastapi import APIRouter, HTTPException, Form
from database.queries import insert_user
from werkzeug.security import generate_password_hash

router = APIRouter()

@router.post("/register")
async def register_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Concatenate first and last names for full name
    full_name = f"{first_name} {last_name}"
    
    # Hash the password for security
    password_hash = generate_password_hash(password)
    
    try:
        # Insert user into the database
        insert_user(full_name, email, password_hash)
        return {"message": "User registered successfully!"}
    except Exception as e:
        # Handle errors
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")
