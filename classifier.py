import ollama
import json
from database import get_prompt


def classify_candidate(candidate_data):

    hr_prompt = get_prompt("classification")

    if not hr_prompt:
        return "Unclassified"

    system_instruction = """
Return strictly in JSON format:

{
  "category": "<result>"
}

Only return JSON.
"""

    final_prompt = f"""
{hr_prompt}

Candidate Data:
Name: {candidate_data['name']}
Location: {candidate_data['location']}
Skills: {candidate_data['skills']}
Resume Text:
{candidate_data['resume_text']}

{system_instruction}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{
            "role": "user",
            "content": final_prompt
        }]
    )

    raw = response["message"]["content"]

    try:
        data = json.loads(raw)
        return data["category"]
    except:
        return "Unclassified"