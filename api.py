from fastapi import FastAPI
from typing import Dict
from processor import classify_candidate

app = FastAPI()

results_store: Dict[int, dict] = {}
current_id = 1


@app.get("/")
def home():
    return {"message": "Resume Screening API is running"}

@app.get("/submit")
def submit_resume(
    name: str,
    location: str,
    skills: str,
    resume_text: str
):
    global current_id

    # Prepare candidate data dictionary
    candidate_data = {
        "name": name,
        "location": location,
        "skills": skills,
        "resume_text": resume_text
    }

    # Call your LLM classifier
    result = classify_candidate(candidate_data)

    # Store result
    results_store[current_id] = {
        "name": name,
        "location": location,
        "skills": skills,
        "result": result
    }

    response = {
        "message": "Resume submitted successfully",
        "candidate_id": current_id
    }

    current_id += 1

    return response

@app.get("/result/{candidate_id}")
def get_result(candidate_id: int):
    if candidate_id not in results_store:
        return {"error": "Candidate not found"}

    return results_store[candidate_id] 