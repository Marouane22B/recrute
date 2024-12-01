from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import users


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
    first_name: str = Form(...), last_name: str = Form(...),
    email: str = Form(...), password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        return {"error": "Passwords do not match!"}
    return {"message": f"Welcome {first_name} {last_name}! Registration successful."}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if email == "test@example.com" and password == "password":
        return {"message": "Login successful!"}
    return {"error": "Invalid credentials. Please try again."}
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

app.include_router(users.router, prefix="/api", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="localhost", port=8000)