from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import difflib
import uvicorn

app = FastAPI()

# Exemple de données d'emplois disponibles
job_database = [
    {"id": 1, "title": "Web Developer", "description": "Develop web applications using modern frameworks like React and Node.js."},
    {"id": 2, "title": "Data Analyst", "description": "Analyze datasets using Python and SQL to derive actionable insights."},
    {"id": 3, "title": "IT Technician", "description": "Provide technical support for hardware and software systems."},
    {"id": 4, "title": "Machine Learning Engineer", "description": "Design and implement machine learning models using Python and TensorFlow."},
    {"id": 5, "title": "Network Administrator", "description": "Maintain and troubleshoot network systems and configurations."},
    {"id": 6, "title": "Software Engineer", "description": "Develop software applications using Java and Spring Boot."},
    {"id": 7, "title": "Product Manager", "description": "Lead product development and manage product lifecycle."}
]

# Modèle pour la requête
class CandidateProfile(BaseModel):
    characteristics: str
    cover_letter: str

# Fonction de recommandation basée sur la similarité
def recommend_jobs(candidate_text: str, jobs: List[Dict]) -> List[Dict]:
    candidate_text = candidate_text.lower().strip()  # Normalisation du texte candidat
    recommendations = []
    for job in jobs:
        job_text = job["description"].lower().strip()  # Normalisation de la description
        # Comparer le texte du candidat avec la description de l'emploi
        similarity = difflib.SequenceMatcher(None, candidate_text, job_text).ratio()
        if similarity > 0.05:  # Seuil de similarité ajustable
            recommendations.append({"job_id": job["id"], "title": job["title"], "similarity": round(similarity, 2)})

    # Trier par similarité décroissante
    recommendations = sorted(recommendations, key=lambda x: x["similarity"], reverse=True)
    return recommendations

@app.post("/recommend-jobs/")
async def recommend_jobs_endpoint(profile: CandidateProfile):
    # Vérifier si les champs sont fournis
    if not profile.characteristics.strip() and not profile.cover_letter.strip():
        raise HTTPException(status_code=400, detail="Les champs 'characteristics' et 'cover_letter' ne peuvent pas être vides.")

    # Combiner les informations pour la recommandation
    candidate_text = f"{profile.characteristics} {profile.cover_letter}"

    # Obtenir les recommandations


    recommendations = recommend_jobs(candidate_text, job_database)

    if not recommendations:
        return {"message": "Aucune recommandation d'emploi trouvée pour ce profil."}

    return {"recommendations": recommendations}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
