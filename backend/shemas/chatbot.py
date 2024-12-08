from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    bot: Optional[str]
    user: Optional[str]

class chatBotParams(BaseModel):
    chatHistory: List[ChatMessage]  # Une liste de messages entre bot et utilisateur
