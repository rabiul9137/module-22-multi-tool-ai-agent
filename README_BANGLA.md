# Module 22 — Multi-Tool AI Agent for Bangladesh

এই project-এ LangChain Agent তিনটি Bangladesh dataset-এর SQLite database এবং একটি web-search tool ব্যবহার করে প্রশ্নের উত্তর দেয়।

## Tools

- `institutions_db_tool` → শিক্ষা ও institutional information
- `hospitals_db_tool` → hospital ও health-institution information
- `restaurants_db_tool` → restaurant, rating, reviews ও address
- `web_search_tool` → general knowledge, policy, definition ও current information

## Run

```bash
pip install -r requirements.txt
python database_setup.py
```

তারপর `.env`-এ `GROQ_API_KEY` সেট করে:

```bash
python main.py
```

## Tested Routing

```text
Hospital question
→ hospitals_db_tool

Educational question
→ institutions_db_tool

Restaurant question
→ restaurants_db_tool

General knowledge
→ web_search_tool
```

Mixed question হলে Agent একাধিক tool ব্যবহার করতে পারে।
