from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
from datasets import load_dataset

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)


def train_dataframe(dataset_name: str) -> pd.DataFrame:
    data = load_dataset(dataset_name)
    split = "train" if "train" in data else next(iter(data.keys()))
    return data[split].to_pandas()


def write_db(df: pd.DataFrame, db_name: str, table_name: str) -> None:
    path = DB_DIR / db_name
    with sqlite3.connect(path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✅ {db_name}: {len(df):,} rows -> table '{table_name}'")


def main() -> None:
    institutions = train_dataframe(
        "Mahadih534/Institutional-Information-of-Bangladesh"
    )
    institutions = institutions.rename(
        columns={
            "INSTITUTE NAME": "name",
            "EIIN": "eiin",
            "INSTITUTE_TYPE": "institute_type",
            "DIVISION_ID": "division_id",
            "DIVISION": "division",
            "DISTRICT_ID": "district_id",
            "DISTRICT": "district",
            "THANA_ID": "thana_id",
            "THANA": "thana",
            "UNION_ID": "union_id",
            "UNION_NAME": "union_name",
            "MAUZA_ID": "mauza_id",
            "MAUZA_NAME": "mauza_name",
            "AREA_STATUS": "area_status",
            "GEOGRPYCAL_STATUS": "geographical_status",
            "ADDRESS": "address",
            "POST": "post",
            "MANAGEMENT_TYPE": "management_type",
            "MOBILE": "mobile",
            "STUDENT_TYPE": "student_type",
            "EDUCATION_LEVEL": "education_level",
            "AFFILIATION": "affiliation",
            "MPO_STATUS": "mpo_status",
        }
    )
    write_db(institutions, "institutions.db", "institutions")

    hospitals = train_dataframe("Mahadih534/all-bangladeshi-hospitals")
    hospitals = hospitals.rename(
        columns={
            "Id": "id",
            "Name": "name",
            "Name (Bangla)": "name_bangla",
            "Code": "code",
            "Agency": "agency",
            "Type": "type",
            "Division": "division",
            "District": "district",
            "City Corporation": "city_corporation",
            "Upazila": "upazila",
            "Paurasava": "paurasava",
            "Union": "union",
            "Private": "private",
        }
    )
    write_db(hospitals, "hospitals.db", "hospitals")

    restaurants = train_dataframe("Mahadih534/Bangladeshi-Restaurant-Data")
    for col in ["latitude", "longitude", "rating", "number_of_reviews"]:
        restaurants[col] = pd.to_numeric(restaurants[col], errors="coerce")
    write_db(restaurants, "restaurants.db", "restaurants")


if __name__ == "__main__":
    main()
