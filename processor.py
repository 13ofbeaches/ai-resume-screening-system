import ollama
import json


def classify_candidate(candidate_data):

    # Read HR editable prompt
    with open("classification_prompt.txt", "r") as f:
        hr_prompt = f.read()

    # Locked system output format
    system_instruction = """
Return your answer strictly in this JSON format:

{
  "category": "<classification_result>"
}

Only return valid JSON.
Do NOT add explanation.
Do NOT add extra text.
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

    raw_output = response["message"]["content"]

    try:
        data = json.loads(raw_output)
        return data["category"]
    except Exception:
        print("⚠ Invalid JSON from LLM.")
        print("Raw output:", raw_output)
        return "Unclassified"