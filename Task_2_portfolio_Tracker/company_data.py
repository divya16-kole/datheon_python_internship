import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
COMPANY_FILE = BASE / "companies.csv"


def load_companies():
    companies = {}

    if not COMPANY_FILE.exists():
        raise FileNotFoundError("companies.csv not found!")

    with open(
        COMPANY_FILE,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("companies.csv is empty.")

        # Clean CSV column names
        reader.fieldnames = [
            name.strip().lstrip("\ufeff")
            for name in reader.fieldnames
        ]

        # Match headers without case sensitivity
        columns = {
            name.strip().lower(): name
            for name in reader.fieldnames
        }

        if "symbol" not in columns or "security" not in columns:
            raise ValueError(
                "CSV must contain Symbol and Security columns."
            )

        for row in reader:
            ticker = (row.get(columns["symbol"]) or "").strip()
            company = (row.get(columns["security"]) or "").strip()

            if not ticker or not company:
                continue

            companies[ticker.upper()] = {
                "company": company,
                "sector": (
                    row.get(columns.get("gics sector", ""), "") or ""
                ).strip(),
                "industry": (
                    row.get(columns.get("gics sub-industry", ""), "") or ""
                ).strip(),
                "location": (
                    row.get(columns.get("headquarters location", ""), "") or ""
                ).strip(),
            }

    return companies


if __name__ == "__main__":
    data = load_companies()
    print("Companies loaded:", len(data))
    print("Sample companies:")

    for ticker, details in list(data.items())[:5]:
        print(ticker, "-", details["company"])
def search_companies(query, companies):
    query = query.strip().lower()

    if not query:
        return []

    matches = []

    for ticker, data in companies.items():
        if query in ticker.lower() or query in data["company"].lower():
            matches.append(ticker)

    return matches        
       