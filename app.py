import json
import os
import glob
import requests
import streamlit as st

OLLAMA_BASE = "http://localhost:11434"
OLLAMA_GEN = f"{OLLAMA_BASE}/api/generate"
OLLAMA_TAGS = f"{OLLAMA_BASE}/api/tags"

DEFAULT_MODEL = "llama3.2:latest"

# Ask the model for STRICT JSON so we can render clean sections in UI
SYSTEM = """You are a ServiceNow Case Copilot.
Return ONLY valid JSON with these keys:
summary (list of strings),
next_actions (list of strings),
engineer_suggestion (string),
customer_reply (string),
risks_or_unknowns (list of strings)

Rules:
- Do NOT invent facts. If information is missing, list it under risks_or_unknowns.
- Keep customer_reply short, professional, and friendly (2–6 lines).
- Make next_actions practical and ordered.
"""

def ollama_is_up() -> bool:
    try:
        r = requests.get(OLLAMA_TAGS, timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def fetch_ollama_models():
    try:
        r = requests.get(OLLAMA_TAGS, timeout=5)
        r.raise_for_status()
        data = r.json()
        models = [m.get("name") for m in data.get("models", []) if m.get("name")]
        return sorted(models)
    except Exception:
        return []

def list_mock_cases(folder="mock_cases"):
    files = sorted(glob.glob(os.path.join(folder, "*.json")))
    return [os.path.splitext(os.path.basename(f))[0] for f in files]

def load_case(case_number: str, folder="mock_cases") -> dict:
    path = os.path.join(folder, f"{case_number}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Mock case not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(case: dict) -> str:
    # Keep it compact: only what the LLM needs
    return f"""{SYSTEM}

CASE DATA:
Number: {case.get("number")}
State: {case.get("state")}
Priority: {case.get("priority")}
Short description: {case.get("short_description")}
Description: {case.get("description")}
Customer comment: {case.get("comments")}
Work notes: {case.get("work_notes")}
""".strip()

def ask_ollama(model: str, prompt: str, temperature: float, top_p: float, num_predict: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "top_p": top_p, "num_predict": num_predict},
    }
    r = requests.post(OLLAMA_GEN, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["response"].strip()

def parse_json_or_fallback(text: str) -> dict:
    # Sometimes models wrap JSON in text. Try to extract the JSON block.
    text_stripped = text.strip()

    # Direct parse first
    try:
        return json.loads(text_stripped)
    except Exception:
        pass

    # Try to find first { ... last }
    start = text_stripped.find("{")
    end = text_stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text_stripped[start:end+1]
        return json.loads(candidate)

    raise ValueError("Model output was not valid JSON. Try again or change model/settings.")

# --- UI ---
st.set_page_config(page_title="ServiceNow Case Copilot", page_icon="🧠", layout="centered")

st.title("🧠 ServiceNow Case Copilot")
st.caption("On-prem LLM copilot for ServiceNow Case Management")

# Simple status line
# Only show status in Advanced view. In Simple view, show nothing unless it's an error.
if not ollama_is_up():
    st.error("Cannot connect to the local AI engine. Please start Ollama and try again.")
    st.stop()

# Toggle advanced view
advanced = st.toggle("Advanced view", value=False)

# Sidebar only when advanced (hide technical stuff by default)
if advanced:
    with st.sidebar:
        st.subheader("⚙️ Model & Controls")
        st.success("Ollama is running ✅")
        models = fetch_ollama_models()
        if models:
            model = st.selectbox("Model", options=models, index=models.index(DEFAULT_MODEL) if DEFAULT_MODEL in models else 0)
        else:
            model = st.text_input("Model", value=DEFAULT_MODEL)

        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
        top_p = st.slider("Top-p", 0.1, 1.0, 0.9, 0.05)
        num_predict = st.slider("Max output tokens", 200, 900, 450, 50)
else:
    # sensible defaults without showing tech controls
    model = DEFAULT_MODEL
    temperature = 0.3
    top_p = 0.9
    num_predict = 450

st.markdown("### Enter Case")
case_ids = list_mock_cases("mock_cases")
default_case = case_ids[0] if case_ids else ""
case_number = st.text_input(
    label="Case number",
    placeholder="CS0001234"
)

generate = st.button("Generate", type="primary", use_container_width=True)

if generate:
    try:
        case = load_case(case_number.strip(), "mock_cases")
        prompt = build_prompt(case)

        with st.spinner("Generating output..."):
            raw = ask_ollama(model, prompt, temperature, top_p, num_predict)
            data = parse_json_or_fallback(raw)

        # Store for advanced view
        st.session_state["last_case"] = case
        st.session_state["last_prompt"] = prompt
        st.session_state["last_raw"] = raw
        st.session_state["last_data"] = data

    except Exception as e:
        st.error(str(e))

data = st.session_state.get("last_data")
case = st.session_state.get("last_case")

if data:
    st.markdown("## Output")

    # Summary
    st.markdown("### ✅ Case Summary")
    for b in data.get("summary", []):
        st.write(f"- {b}")

    # Next Actions
    st.markdown("### 🧭 Next Actions")
    for a in data.get("next_actions", []):
        st.write(f"- {a}")

    # Engineer Suggestion
    st.markdown("### 🛠️ Engineer Suggestion (Work Notes Draft)")
    st.text_area("Engineer Suggestion", value=data.get("engineer_suggestion", ""), height=120)

    # Customer Reply “popup-like”
    with st.expander("💬 Customer Reply Draft (Click to view/copy)"):
        st.text_area("Customer Reply", value=data.get("customer_reply", ""), height=140)

    # Risks / Unknowns
    risks = data.get("risks_or_unknowns", [])
    if risks:
        st.markdown("### ⚠️ Missing Info / Risks")
        for r in risks:
            st.write(f"- {r}")

    # Advanced debug section
    if advanced:
        st.markdown("---")
        st.markdown("## Advanced Details")
        st.markdown("### Raw JSON")
        st.code(json.dumps(data, indent=2), language="json")

        st.markdown("### Prompt")
        st.code(st.session_state.get("last_prompt", ""), language="text")

        st.markdown("### Case JSON used")
        st.json(case)
