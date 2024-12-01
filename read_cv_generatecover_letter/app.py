from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from transformers import pipeline
import pdfplumber
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Flan-T5 model


# Charger un modèle pré-entraîné plus robuste
pipe = pipeline("text2text-generation", model="t5-small", device=-1)  # Utilisation du CPU
pipe.tokenizer.pad_token_id = pipe.model.config.eos_token_id  # Configurer pad_token_id


# Extract text from PDF
def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    try:
        with pdfplumber.open(pdf_file.file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {e}")

# Extract key characteristics
def extract_key_characteristics(text: str) -> List[str]:
    prompt = (
        f"Analyze the following text: {text}. "
        "Extract exactly 5 key characteristics or skills of the person, each limited to a maximum of 5 words."
    )
    result = pipe(prompt, max_new_tokens=50, num_return_sequences=1)
    generated_text = result[0]['generated_text']
    
    # Process the response to extract characteristics as a list
    characteristics = [char.strip() for char in generated_text.split("\n") if char.strip()]
    characteristics = characteristics[:5]  # Limit to 5 characteristics
    joined_characteristics = ", ".join(characteristics)
    return joined_characteristics


# Generate a cover letter
def generate_cover_letter(text: str) -> str:
    prompt = f"Based on this text: {text}. Generate a professional cover letter."
    result = pipe(prompt, max_new_tokens=150, num_return_sequences=1)
    return result[0]['generated_text']

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)) -> Dict[str, str]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="The file must be a PDF.")

    pdf_text = extract_text_from_pdf(file)

    if not pdf_text.strip():
        raise HTTPException(status_code=400, detail="The PDF appears empty or unreadable.")

    characteristics = extract_key_characteristics(pdf_text)
    cover_letter = generate_cover_letter(pdf_text)

    return {
        "characteristics": characteristics,
        "cover_letter": cover_letter
    }

chat_history: List[Dict[str, str]] = []

@app.post("/chatbot/")
async def chatbot_interaction(message: str = Form(...)) -> Dict[str, object]:
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    chat_history.append({"sender": "You", "message": message})

    prompt = (
        f"Based on the following message: {message}. "
        "Help the user and provide a response."
    )
    result = pipe(prompt, max_new_tokens=100, num_return_sequences=1)
    response = result[0]['generated_text']

    chat_history.append({"sender": "Bot", "message": response})

    return {"response": response, "history": chat_history}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
