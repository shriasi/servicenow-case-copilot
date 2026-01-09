import json
import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"  # you already have this

SYSTEM_INSTRUCTIONS = """You are a ServiceNow Case Copilot.
Given a ServiceNow case, produce:

CASE SUMMARY:
- 3-6 bullets

CUSTOMER UPDATE DRAFT:
- Short, professional (2-6 lines)

NEXT ACTIONS:
- Checklist bullets

CLARIFYING QUESTIONS (if needed):
- bullets

Rules:
- Do NOT invent facts. If missing, ask questions.
- Keep customer update confident and simple.
"""

def ask_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "top_p": 0.9, "num_predict": 450}
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["response"].strip()

def load_case(case_number: str) -> dict:
    path = os.path.join("mock_cases", f"{case_number}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Mock case not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(case: dict) -> str:
    return f"""{SYSTEM_INSTRUCTIONS}

CASE DATA:
Number: {case.get("number")}
State: {case.get("state")}
Priority: {case.get("priority")}
Short description: {case.get("short_description")}
Description: {case.get("description")}
Customer comment: {case.get("comments")}
Work notes: {case.get("work_notes")}
""".strip()

if __name__ == "__main__":
    print("ServiceNow Case Copilot (Mock Mode) - Ollama\n")
    case_number = input("Enter Case number (e.g., CS0001234): ").strip()
    case = load_case(case_number)
    prompt = build_prompt(case)
    output = ask_ollama(prompt)
    print("\n" + output)
