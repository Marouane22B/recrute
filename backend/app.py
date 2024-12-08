import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from utils.class_object import singleton

# Route Imports
from routes.auth import auth_router
from routes.chatbot import chat_router

@singleton
class App:
    def __init__(self) -> None:
        self.app = FastAPI(
            title="Moderation content API",
            description="API for moderation content",
            debug=True)
        # Set the database connection
        
        # Set CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Set Static Files public dans la racine du projet
        self.app.mount("/public", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'public')), name="public")

        # Set Routes
        self.app.include_router(auth_router)
        self.app.include_router(chat_router)

    # GET app
    def get_app(self):
        return self.app
        
app = App().get_app()

if __name__ == "__main__":
    # Run the server
    print(f"Running server on 0.0.0.0:8000")
    uvicorn.run(
        "app:app",
        host="localhost",
        port=8000,
        reload=True)