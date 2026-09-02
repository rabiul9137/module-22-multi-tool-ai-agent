# 🇧🇩 Multi-Tool AI Agent for Bangladesh

A LangChain-based AI agent that answers Bangladesh-specific questions using three SQLite databases and a web search tool.

## Features

- Educational/institutional queries via `institutions.db`
- Hospital and health-institution queries via `hospitals.db`
- Restaurant queries via `restaurants.db`
- General knowledge and current-information queries via web search (`ddgs`)
- Groq LLM with tool calling
- LangChain Agent Executor with automatic tool routing
- Read-only SQL validation for database tools

## Dataset Sources

- Institutional Information of Bangladesh: `Mahadih534/Institutional-Information-of-Bangladesh`
- All Bangladeshi Hospitals: `Mahadih534/all-bangladeshi-hospitals`
- Bangladeshi Restaurant Data: `Mahadih534/Bangladeshi-Restaurant-Data`

## Project Structure

```text
module-22-multi-tool-ai-agent/
├── database/
│   └── *.db                  # generated locally
├── tools/
│   ├── __init__.py
│   ├── db_tools.py
│   └── web_search.py
├── database_setup.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd module-22-multi-tool-ai-agent
```

### 2. Install dependencies

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Groq

Create `.env` from `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit `.env` or expose your API key.

### 4. Create the SQLite databases

```bash
python database_setup.py
```

This creates:

- `database/institutions.db`
- `database/hospitals.db`
- `database/restaurants.db`

### 5. Run the agent

```bash
python main.py
```

## Example Questions

```text
How many health institutions are in Dhaka?
Find 5 educational institutions in Dhaka.
Show me 5 highly rated restaurants.
What is the role of DGHS in Bangladesh?
Find 5 health institutions in Dhaka and explain the role of DGHS in Bangladesh.
```

## Verified Demo Behavior

During testing, the agent successfully routed:

- Hospital questions -> `hospitals_db_tool`
- Educational institution questions -> `institutions_db_tool`
- Restaurant questions -> `restaurants_db_tool`
- General DGHS questions -> `web_search_tool`
- Mixed questions -> multiple tools in one execution

A tested hospital query returned 9,876 records for `district = 'Dhaka'` in the provided hospital/health-institution dataset.

## Notes

The hospital dataset contains a mixture of health facilities, offices, and public-health institutions, so the project describes it as a health-institution dataset rather than assuming every row is a traditional hospital.

The web-search component uses `ddgs`, which provides a direct `DDGS().text(...)` interface and does not require a Tavily API key.
