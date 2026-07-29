# scripts/fetch_contributions.py
import json
import requests

def fetch_contributions(username="Rida1019-taki", output_file="data/contributions.json"):
    url = f"https://github-contributions-api.jogruber.de/v4/{username}?y=last"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            days = []
            for item in data.get("contributions", []):
                days.append({
                    "date": item.get("date"),
                    "level": item.get("count") # Map directly
                })

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({"days": days}, f, indent=2)
            print("Contributions fetched successfully!")
        else:
            print("Failed to fetch API")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_contributions()