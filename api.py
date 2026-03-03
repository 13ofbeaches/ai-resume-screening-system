from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import (
    get_all_candidates,
    insert_candidate,
    update_candidate_category
)

from processor import classify_candidate


app = FastAPI()

# ✅ Enable CORS so Next.js can call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Resume Screening API is running"}


# 🔹 Submit Resume Endpoint
@app.get("/submit")
def submit_resume(
    name: str,
    email: str,
    phone: str,
    location: str,
    skills: str,
    resume_text: str
):

    # Step 1 — Insert candidate into DB
    candidate_id = insert_candidate(
        name=name,
        email=email,
        phone=phone,
        location=location,
        s3_url="manual_upload",
        skills=skills
    )

    # Step 2 — Run AI classification
    candidate_data = {
        "name": name,
        "location": location,
        "skills": skills,
        "resume_text": resume_text
    }

    category = classify_candidate(candidate_data)

    # Step 3 — Update DB with classification result
    update_candidate_category(candidate_id, category)

    return {
        "message": "Resume submitted successfully",
        "candidate_id": candidate_id,
        "category": category
    }


# 🔹 Get All Candidates (Metadata + Result)
@app.get("/candidates")
def get_candidates():
    data = get_all_candidates()

    return {
        "total_candidates": len(data),
        "data": data
    }