import json
import os
import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

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

st.set_page_config(page_title="ServiceNow Case Copilot", page_icon="🧠", layout="centered")
st.title("🧠 ServiceNow Case Copilot (Local)")
st.caption("Mock mode + Ollama (no paid APIs). Generate a case summary + customer update draft.")

case_number = st.text_input("Case number", placeholder="CS0001234")
run = st.button("Generate")

with st.expander("Settings"):
    MODEL = st.text_input("Ollama model", value=MODEL)
    st.write("Tip: keep Ollama running (localhost:11434).")

if run:
    if not case_number.strip():
        st.warning("Please enter a case number (e.g., CS0001234).")
    else:
        try:
            case = load_case(case_number.strip())
            prompt = build_prompt(case)

            with st.spinner("Generating with Ollama..."):
                output = ask_ollama(prompt)

            st.subheader("✅ Output")
            st.text_area("Result", value=output, height=340)

            with st.expander("📄 Case data used (mock)"):
                st.json(case)

        except Exception as e:
            st.error(str(e))
