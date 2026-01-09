ServiceNow Case Copilot 🧠

A beginner-friendly, onsite-hosted AI copilot for ServiceNow Case / Incident Management,
powered by a local Large Language Model (LLM) 

This solution analyzes a ServiceNow case and provides:
- A clear case summary
- Suggested next actions
- Engineer work-note recommendations
- A customer reply draft (ready to copy)

The tool runs fully locally, uses no paid APIs, and is designed for privacy-sensitive
enterprise environments.

It is architected to be integrated into ServiceNow (SNOW) as an onsite AI copilot
for Incident and Case Management.

--------------------------------------------------

KEY FEATURES

- Case Summary
  Condenses long case descriptions and updates into short, clear bullet points.

- Next Action Suggestions
  Provides practical and ordered steps engineers can follow.

- Engineer Suggestion
  Drafts internal work notes based on the case context.

- Customer Reply Draft
  Generates a professional, friendly customer response shown in a popup-style section.

- Onsite / Local LLM
  Uses a locally hosted model via Ollama. No data leaves the machine.

- Simple UI + Advanced Toggle
  Default UI is clean and non-technical.
  Advanced view exposes model settings, prompts, and raw JSON for engineers.

--------------------------------------------------

USER INTERFACE DESIGN

SERVICE NOW INTEGRATION POTENTIAL

This solution is designed to be easily integrated into ServiceNow (SNOW) environments.

Possible integration approaches include:
- ServiceNow UI Action or UI Page embedding
- ServiceNow Workspace integration (Agent / CSM workspace)
- REST API-based read-only access to Incidents / Cases
- Controlled write-back to comments or work notes with confirmation

The current implementation runs in mock mode for safety and learning purposes,
but the architecture supports direct ServiceNow API integration in enterprise
environments.

Simple View (Default)
- Enter case number
- Click Generate
- View AI-generated output

Advanced View (Toggle)
- Model selection and tuning
- Raw prompt and JSON output
- Case data inspection for debugging

This design keeps the UI easy for end users while still supporting technical exploration.

--------------------------------------------------

MOCK MODE (SAFE FOR GITHUB)

This repository uses mock ServiceNow case data stored as JSON files.

- No real ServiceNow credentials
- No customer or production data
- Safe for demos, learning, and public sharing

Example mock case file:
mock_cases/CS0001234.json

--------------------------------------------------

TECH STACK

- Python 3.10+
- Ollama (local LLM runtime)
- Open-source LLMs (e.g. llama3.2, gemma)
- Streamlit (UI)
- Requests (HTTP client)

--------------------------------------------------

GETTING STARTED

1. Prerequisites
- Python 3.10 or higher
- Ollama installed and running
- At least one Ollama model pulled

Example:
ollama pull llama3.2:latest

--------------------------------------------------

2. Install dependencies
pip install streamlit requests

--------------------------------------------------

3. Run the application
streamlit run app.py

The UI will open in your browser.

--------------------------------------------------

EXAMPLE WORKFLOW

1. Enter a case number (e.g. CS0001234)
2. Click Generate
3. Review:
   - Case summary
   - Next actions
   - Engineer suggestion
4. Open the Customer Reply Draft and copy it into ServiceNow

--------------------------------------------------

SECURITY & PRIVACY

- Runs fully locally / onsite
- No external API calls
- No data sent outside the environment
- Designed for enterprise and internal usage

--------------------------------------------------

ROADMAP / FUTURE ENHANCEMENTS

- Knowledge Base grounding (RAG over internal KB / runbooks)
- Real ServiceNow API integration (read-only first)
- Controlled write-back (comments / work notes)
- Confidence scoring and explainability
- Deeper ServiceNow UI integration

--------------------------------------------------

AUTHOR

Shrimali Senevirathna

--------------------------------------------------

CONTRIBUTIONS

Ideas, feedback, and improvements are welcome.

--------------------------------------------------

LICENSE

MIT License
