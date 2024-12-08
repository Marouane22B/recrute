from shemas.chatbot import chatBotParams
from utils.class_object import singleton
import requests
from typing import Dict
from pydantic import BaseModel



@singleton
class ChatbotController:
    def __init__(self, model_name: str = "llama3", api_url: str = "http://127.0.0.1:8011/api/chat"):
        """
        Initialise le chatbot Ollama.

        Args:
            model_name (str): Nom du modèle Ollama à utiliser (par défaut : "llama2").
            api_url (str): URL de l'API Ollama (par défaut : "http://localhost:11434/api/chat").
        """
        self.model_name = model_name
        self.api_url = api_url
    
   
    
    async def chat(self, params: chatBotParams):
        """
        Interagit avec le modèle Ollama et retourne la réponse.

        Args:
            params (ChatBotParams): Les paramètres contenant le message utilisateur.

        Returns:
            Dict: La réponse générée par Ollama.
        """
        try:
            # Préparer les données pour l'API Ollama
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": str(params.model_dump(exclude_none=True))}]
            }
            # Envoyer la requête POST
            response = requests.post(self.api_url, json=payload)

            # Vérifier le statut de la réponse
            if response.status_code != 200:
                raise Exception(f"Erreur API Ollama : {response.status_code} - {response.text}")

            # Extraire et retourner la réponse du modèle
            response_data = response.json()
            print(response_data)
            bot_response = response_data.get("content", "Aucune réponse générée.")
            return {
                "status": "success",
                "user_message": params.message,
                "bot_response": bot_response
            }

        except Exception as e:
            # Gérer les erreurs
            print(f"Erreur dans la méthode chat : {e}")
            return {
                "status": "error",
                "message": str(e)
            }    
