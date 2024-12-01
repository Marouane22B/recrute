import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import users
from database.connection import get_snowflake_connection
from fastapi import FastAPI, Form, HTTPException
from werkzeug.security import generate_password_hash
from database.queries import get_user_by_email, insert_user

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

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


@app.get("/dashbord", response_class=HTMLResponse)
async def dashbord_page(request: Request):
    # Récupérer le cookie utilisateur
    user_cookie = request.cookies.get("user")
    user = json.loads(user_cookie) if user_cookie else None
    
    # Passer l'utilisateur au template
    return templates.TemplateResponse("dashbord.html", {"request": request, "user": user})

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)

    if user:  # Assurez-vous que l'utilisateur existe et que le mot de passe est correct.
        redirect_url = "/dashbord"
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.set_cookie(key="user", value=json.dumps(user), httponly=True)
        return response
    else:
        # Redirigez vers une page d'erreur ou retournez un message d'erreur.
        return {"error": "Invalid credentials"}


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@app.post("/chatbot/")
async def chatbot_interaction(message: str = Form(...), request: Request = None):
    user_cookie = request.cookies.get("user")
    user = json.loads(user_cookie) if user_cookie else None

    if not user:
        return {"error": "Unauthorized access. Please log in first."}

    # Vérifiez si le message concerne la recherche d'emploi
    job_keywords = ["job", "employment", "recruitment", "career"]
    if any(keyword in message.lower() for keyword in job_keywords):
        # Simulez une réponse du chatbot
        response = {
            "user": user.get("email"),
            "message": message,
            "response": "Thank you for your inquiry! How can I assist you with your job search?"
        }
        # Stockez l'historique si nécessaire (simulation ici)
        return response
    else:
        return {"error": "This chatbot only handles job-related inquiries."}


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