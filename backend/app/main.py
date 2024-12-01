from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import users
from database.connection import get_snowflake_connection
from fastapi import FastAPI, Form, HTTPException
from werkzeug.security import generate_password_hash
from database.queries import insert_user


# Création de l'application FastAPI
app = FastAPI()

# Configuration des fichiers statiques et des templates
app.mount("/static", StaticFiles(directory="../frontend/public"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    confirm_password: str = Form(...), 
    role: str = Form("candidat")
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    # Hash du mot de passe pour la sécurité
    password_hash = generate_password_hash(password)
    try:
        # Insérer l'utilisateur dans la base de données
        insert_user(name, email, password_hash, role)
        return {"message": "User registered successfully!"}
    except Exception as e:
        # Gestion des erreurs
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    # Vérifier les informations d'identification
    user = get_user_by_email(email)
    if user:
        if check_password_hash(user["password"], password):
            return {"message": "User logged in successfully!"}
    else:

    return {"error": "Invalid credentials. Please try again."}



@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

app.include_router(users.router, prefix="/api", tags=["users"])
try:
    conn = get_snowflake_connection()
    print("Connexion à Snowflake réussie !")
    conn.close()
except Exception as e:
    print(f"Erreur lors de la connexion à Snowflake : {e}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="localhost", port=8000)