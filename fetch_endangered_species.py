import requests
import pandas as pd
import time
import os

# Get list of all GBIF-supported countries
def get_supported_countries():
    url = "https://api.gbif.org/v1/enumeration/country"
    response = requests.get(url)
    countries = response.json()
    return {c["iso2"]: c["title"] for c in countries if len(c["iso2"]) == 2}

# Fetch occurrences of threatened species per country
def fetch_gbif_data(country_code, limit_per_country=200):
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
        return data.get("results", [])
    except Exception as e:
        print(f"Error fetching data for {country_code}: {e}")
        return []

# Parse result list into dataframe
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
            "event_date": r.get("eventDate")
        })
    return pd.DataFrame(rows)

# MAIN FUNCTION
if __name__ == "__main__":
    all_data = []
    country_map = get_supported_countries()

    # Use only first 30 countries for speed while testing
    selected_countries = list(country_map.keys())[:30]

    print(f"🌐 Fetching data for {len(selected_countries)} countries...")

    for code in selected_countries:
        print(f"🔎 {country_map[code]} ({code})")
        results = fetch_gbif_data(code)
        if results:
            df = parse_results(results, code)
            all_data.append(df)
        time.sleep(0.5)  # avoid hitting rate limits

    # Combine and save
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        os.makedirs("data", exist_ok=True)
        final_df.to_csv("data/gbif_threatened_species.csv", index=False)
        print(f"\n✅ Data saved to data/gbif_threatened_species.csv")
        print(f"🔢 Total records: {len(final_df)}")
        print(f"🌍 Countries included: {final_df['country'].nunique()}")
