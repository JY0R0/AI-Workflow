from pdfminer.high_level import extract_text
import requests
import fitz

def pdf_to_text(file_path):
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def generate_prompt(resume_text):
    return f"""
You are an AI that extracts structured work experience data from resumes. 
Your job is to return **only valid JSON**, exactly in the following format:

{{
  "name": "Candidate Name",
  "experiences": [
    {{
      "company": "Company 1",
      "title": "Job Title 1",
      "start_date": "Month Year",
      "end_date": "Month Year or Present"
    }},
    ...
  ]
}}

Rules:
- If some values (like end_date) are missing, use null.
- Do NOT add comments or explanation.
- Do NOT wrap JSON in markdown.

Resume Text:
\"\"\"{resume_text}\"\"\"
"""

import json
import re
from ollama import Client

ollama = Client(host='http://localhost:11434') 
def fix_json_like_output(text):
    text = re.sub(r"```(?:json)?", "", text)
    text = text.replace("'", '"')
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)
    return text.strip()

def extract_experience(resume_text):
    prompt = generate_prompt(resume_text)

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}]).get("message", {}).get("content", "")

#response log
    print("\n--- Raw LLaMA Output ---\n", response)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("❌ JSON parsing failed. Attempting fix...")
        fixed = fix_json_like_output(response)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            print("❌ Even fixed JSON failed. Saving for review.")
            with open("error_response.txt", "w", encoding="utf-8") as f:
                f.write(response)
            return None