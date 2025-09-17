from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class ChatRequest(BaseModel):
    query : str
    chat_history : list[dict[str,str]]|None = None
 
@app.get('/')
def read_root():
    return {"success" : True,
            "message" : "Server is running!"}

@app.post('/chat')
def handle_chat(request : ChatRequest):
    if not request or not request.query:
        return {'success' : False,
                'message' : 'User query required'}
    
    ai_response = chatbot(request.query, request.chat_history)

    if not ai_response:
        return {'success' : False,
                'message' : "Error getting ai reponse"}
    
    return {'success' : True,
            'message' : "ai reponse fetched successfully",
            'response' : ai_response}


