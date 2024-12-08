from fastapi import APIRouter, status
from controllers.chatbot import ChatbotController
from shemas.auth import *
from shemas.chatbot import chatBotParams

chat_router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"])

chat_controller = ChatbotController()


@chat_router.post("/chat", status_code=status.HTTP_200_OK)
async def chatbot(params: chatBotParams):
    return await chat_controller.chat(params)
