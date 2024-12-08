import pdfplumber  # Pour extraire le texte du PDF
import requests  # Pour interagir avec Ollama
from fpdf import FPDF  # FPDF2 pour générer le PDF
from fastapi import UploadFile
from utils.class_object import singleton

@singleton
class JobsController:
    def __init__(self):
        # URL de l'API Ollama (serveur local)
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.model_name = "llama3"

    async def extract_data_from_cv(self, cv: UploadFile):
        """
        Cette fonction extrait le texte d'un fichier PDF de CV et génère une lettre de motivation.

        Args:
            cv (UploadFile): Le fichier de CV à traiter.

        Returns:
            dict: Un dictionnaire contenant le contenu du CV et la lettre de motivation générée.
        """
        try:
            # 1️⃣ Extraire le texte du CV
            content = await self.extract_text_from_pdf(cv)
            print(f"Contenu du CV extrait ({len(content)} caractères)")

            # 2️⃣ Extraire les informations importantes du CV
            extracted_info = self.extract_key_information(content)
            print(f"Informations extraites du CV : {extracted_info}")

            # 3️⃣ Générer la lettre de motivation avec Ollama
            cover_letter = await self.generate_cover_letter_with_ollama(extracted_info)

            # 4️⃣ Générer le fichier PDF de la lettre de motivation
            pdf_path = self.generate_pdf_cover_letter(cover_letter, extracted_info)
            print(f"Lettre de motivation PDF générée : {pdf_path}")

            return {
                "status": "success",
                "cv_content": content,
                "extracted_info": extracted_info,
                "cover_letter": cover_letter,
                "pdf_path": pdf_path
            }

        except Exception as e:
            print(f"Erreur lors de l'extraction du CV ou de la génération de la lettre de motivation : {e}")
            return {"status": "error", "message": str(e)}

    async def extract_text_from_pdf(self, cv: UploadFile) -> str:
        """
        Extrait le texte d'un fichier PDF à l'aide de pdfplumber.
        
        Args:
            cv (UploadFile): Le fichier de CV téléchargé.

        Returns:
            str: Le contenu complet du PDF sous forme de texte brut.
        """
        content = ""
        try:
            pdf_bytes = await cv.read()
            with pdfplumber.open(cv.file) as pdf:
                for page in pdf.pages:
                    content += page.extract_text()
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte du PDF : {e}")
            raise e
        
        return content

    def extract_key_information(self, content: str) -> dict:
        """
        Extrait les informations importantes du contenu du CV.

        Args:
            content (str): Le texte brut du CV.

        Returns:
            dict: Les informations importantes extraites du CV.
        """
        extracted_info = {}

        try:
            if "Nom" in content:
                extracted_info["name"] = content.split("Nom")[1].split("\n")[0].strip()
            if "Email" in content:
                extracted_info["email"] = content.split("Email")[1].split("\n")[0].strip()
            if "Téléphone" in content:
                extracted_info["phone"] = content.split("Téléphone")[1].split("\n")[0].strip()
        except Exception as e:
            print(f"Erreur lors de l'extraction des informations du CV : {e}")
        
        return extracted_info

    async def generate_cover_letter_with_ollama(self, extracted_info: dict) -> str:
        """
        Génère une lettre de motivation à partir des informations extraites du CV en utilisant Ollama.

        Args:
            extracted_info (dict): Les informations extraites du CV.

        Returns:
            str: La lettre de motivation générée.
        """
        try:
            prompt = f"""
            Écrivez une lettre de motivation personnalisée pour {extracted_info.get('name', 'un candidat')}. 
            Le candidat peut être contacté à l'adresse e-mail {extracted_info.get('email', 'inconnue')} 
            et au téléphone {extracted_info.get('phone', 'inconnu')}. 
            Le texte doit expliquer pourquoi le candidat est qualifié pour le poste et inclure des arguments convaincants.
            """

            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('content', 'Aucune lettre de motivation générée.')
            else:
                print(f"Erreur de réponse de Ollama : {response.status_code} - {response.text}")
                return "Erreur lors de la génération de la lettre de motivation."

        except Exception as e:
            print(f"Erreur lors de la génération de la lettre de motivation : {e}")
            return "Erreur lors de la génération de la lettre de motivation."

    def generate_pdf_cover_letter(self, cover_letter: str, extracted_info: dict) -> str:
        """
        Génère un fichier PDF de la lettre de motivation.

        Args:
            cover_letter (str): Le contenu de la lettre de motivation.
            extracted_info (dict): Les informations de l'utilisateur (nom, e-mail, téléphone).

        Returns:
            str: Le chemin du fichier PDF généré.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # En-tête
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(0, 10, f"Lettre de Motivation - {extracted_info.get('name', 'Candidat')}", ln=True, align="C")
        pdf.ln(10)  # Saut de ligne

        # Informations de l'utilisateur
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Nom: {extracted_info.get('name', 'Non précisé')}", ln=True)
        pdf.cell(0, 10, f"Email: {extracted_info.get('email', 'Non précisé')}", ln=True)
        pdf.cell(0, 10, f"Téléphone: {extracted_info.get('phone', 'Non précisé')}", ln=True)
        pdf.ln(10)  # Saut de ligne

        # Contenu de la lettre de motivation
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, cover_letter)
        
        # Chemin où enregistrer le fichier PDF
        pdf_path = f"cover_letters/cover_letter_{extracted_info.get('name', 'candidat')}.pdf"
        
        try:
            pdf.output(pdf_path)
        except Exception as e:
            print(f"Erreur lors de la création du fichier PDF : {e}")
            raise e
        
        return pdf_path
