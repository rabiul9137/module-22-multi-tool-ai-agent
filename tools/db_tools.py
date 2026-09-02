import os
import re
import sqlite3

import pandas as pd
from langchain_core.tools import tool


# Database paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

INSTITUTIONS_DB = os.path.join(DATABASE_DIR, "institutions.db")
HOSPITALS_DB = os.path.join(DATABASE_DIR, "hospitals.db")
RESTAURANTS_DB = os.path.join(DATABASE_DIR, "restaurants.db")


def _validate_sql(query: str) -> str:
    """Allow read-only SQLite queries only."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("SQL query cannot be empty.")

    query = query.strip()

    query = re.sub(
        r"^```(?:sql)?\s*",
        "",
        query,
        flags=re.IGNORECASE
    )

    query = re.sub(r"\s*```$", "", query)

    if not re.match(r"^(SELECT|WITH)\b", query, re.IGNORECASE):
        raise ValueError("Only SELECT/WITH queries are allowed.")

    forbidden = re.compile(
        r"\b("
        r"INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|"
        r"REPLACE|TRUNCATE|ATTACH|DETACH|PRAGMA"
        r")\b",
        re.IGNORECASE
    )

    if forbidden.search(query):
        raise ValueError("Unsafe SQL operation detected.")

    statements = [
        statement.strip()
        for statement in query.split(";")
        if statement.strip()
    ]

    if len(statements) > 1:
        raise ValueError("Only one SQL statement is allowed.")

    return query


def _run_query(db_path: str, query: str) -> str:
    """Execute a read-only SQL query."""

    try:
        query = _validate_sql(query)

        if not os.path.exists(db_path):
            return (
                "Database not found. "
                "Please run database_setup.py first."
            )

        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return "No results found."

        if len(df) > 50:
            df = df.head(50)

        return df.to_string(index=False)

    except Exception as e:
        return f"Database error: {str(e)}"


@tool
def institutions_db_tool(query: str) -> str:
    """
    Query the Bangladesh educational and institutional database.

    Table: institutions

    Columns:
    name, eiin, institute_type, division_id, division,
    district_id, district, thana_id, thana, union_id,
    union_name, mauza_id, mauza_name, area_status,
    geographical_status, address, post, management_type,
    mobile, student_type, education_level, affiliation,
    mpo_status.
    """
    return _run_query(INSTITUTIONS_DB, query)


@tool
def hospitals_db_tool(query: str) -> str:
    """
    Query the Bangladesh hospitals and health institutions database.

    Table: hospitals

    Columns:
    id, name, name_bangla, code, agency, type, division,
    district, city_corporation, upazila, paurasava,
    union, private.

    Important:
    There is NO 'city' column.
    """
    return _run_query(HOSPITALS_DB, query)


@tool
def restaurants_db_tool(query: str) -> str:
    """
    Query the Bangladeshi restaurant database.

    Table: restaurants

    Columns:
    place_id, name, latitude, longitude, rating,
    number_of_reviews, affluence, address.
    """
    return _run_query(RESTAURANTS_DB, query)
