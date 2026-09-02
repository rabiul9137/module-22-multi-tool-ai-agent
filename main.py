from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

from tools.db_tools import (
    hospitals_db_tool,
    institutions_db_tool,
    restaurants_db_tool,
)
from tools.web_search import web_search_tool

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Set it in .env or your environment.")

model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

llm = ChatGroq(
    api_key=api_key,
    model=model_name,
    temperature=0,
)

tools = [
    institutions_db_tool,
    hospitals_db_tool,
    restaurants_db_tool,
    web_search_tool,
]

SYSTEM_PROMPT = """
You are a Bangladesh-focused Multi-Tool AI Assistant.

TOOLS
1. institutions_db_tool: educational/institutional data.
2. hospitals_db_tool: hospitals and health institutions.
3. restaurants_db_tool: restaurant data.
4. web_search_tool: general knowledge, policies, definitions, culture, and current information.

EXACT SCHEMAS
institutions:
name, eiin, institute_type, division_id, division, district_id, district,
thana_id, thana, union_id, union_name, mauza_id, mauza_name, area_status,
geographical_status, address, post, management_type, mobile, student_type,
education_level, affiliation, mpo_status

hospitals:
id, name, name_bangla, code, agency, type, division, district,
city_corporation, upazila, paurasava, union, private

restaurants:
place_id, name, latitude, longitude, rating, number_of_reviews,
affluence, address

ROUTING
- Educational institution -> institutions_db_tool
- Hospital/health institution -> hospitals_db_tool
- Restaurant -> restaurants_db_tool
- General/current/policy/definition -> web_search_tool
- Use multiple tools when the question requires multiple sources.

SQL RULES
- Use only SELECT/WITH queries.
- Never invent column names.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE or PRAGMA.
- For Dhaka hospitals use district/division/city_corporation/upazila, never a nonexistent 'city' column.
- For institutions use division/district/thana.
- For restaurants use address for location filtering.
- Use COUNT(*) for counting and LIMIT for list queries.

ANSWER RULES
Return a concise, accurate natural-language answer based on tool results.
Do not invent facts that are not in the database or retrieved search results.
Clearly distinguish database information from web information.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=6,
)


def run_agent(question: str) -> str:
    result = agent_executor.invoke({"input": question})
    return result["output"]


def main() -> None:
    print("\n🇧🇩 Bangladesh Multi-Tool AI Agent")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        try:
            print("\nAgent:", run_agent(question), "\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    main()
