import requests
import pandas as pd
import time
import os
from concurrent.futures import ThreadPoolExecutor

# === Helper Functions ===

def get_supported_countries():
    url = "https://api.gbif.org/v1/enumeration/country"
    response = requests.get(url)
    countries = response.json()
    return {c["iso2"]: c["title"] for c in countries if len(c["iso2"]) == 2}

def fetch_gbif_data(country_code, limit_per_country=300):
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "country": country_code,
        "threatStatus": "Threatened",
        "limit": limit_per_country,
        "hasCoordinate": "true"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"❌ Error {response.status_code} for {country_code}")
            return []
        data = response.json()
        print(f"✅ Retrieved {len(data.get('results', []))} for {country_code}")
        return data.get("results", [])
    except Exception as e:
        print(f"❌ Exception for {country_code}: {e}")
        return []

def parse_results(results, country_code):
    rows = []
    for r in results:
        rows.append({
            "species": r.get("species"),
            "class": r.get("class"),
            "country": country_code,
            "threat_status": r.get("threatStatus"),
            "latitude": r.get("decimalLatitude"),
            "longitude": r.get("decimalLongitude"),
            "event_date": r.get("eventDate"),
            "scientificName": r.get("scientificName"),
            "commonName": r.get("vernacularName")
        })
    return pd.DataFrame(rows)

# === Main ===

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    all_data = []
    country_map = get_supported_countries()
    selected_countries = list(country_map.keys())

    print(f"🌍 Fetching data for {len(selected_countries)} countries...")

    for code in selected_countries:
        results = fetch_gbif_data(code)
        if results:
            df = parse_results(results, code)
            all_data.append(df)
        time.sleep(0.2)  # polite rate limiting

    if not all_data:
        print("❌ No data fetched.")
        exit()

    df = pd.concat(all_data, ignore_index=True)
    before = len(df)
    df.drop_duplicates(subset=["species", "country", "latitude", "longitude"], inplace=True)
    after = len(df)
    print(f"🧹 Removed {before - after} duplicate records")

    df.to_csv("data/gbif_threatened_species_raw.csv", index=False)
    print(f"\n💾 Raw data saved to data/gbif_threatened_species_raw.csv")
