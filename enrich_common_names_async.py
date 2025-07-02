import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def fetch_common_name(scientific_name):
    url = f"https://api.gbif.org/v1/species/match?name={scientific_name}"
    try:
        match = requests.get(url).json()
        if not match or "usageKey" not in match:
            return None
        key = match["usageKey"]
        vernaculars = requests.get(f"https://api.gbif.org/v1/species/{key}/vernacularNames").json()
        names = vernaculars.get("results", [])
        for name in names:
            if name.get("language") == "eng":
                return name.get("vernacularName")
        return names[0].get("vernacularName") if names else None
    except:
        return None

def enrich_common_names(scientific_names, max_workers=16):
    results = {}

    def task(name):
        if pd.isna(name):
            return None, None
        return name, fetch_common_name(name)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task, name): name for name in scientific_names}
        for future in as_completed(futures):
            name, common = future.result()
            if name and common:
                results[name] = common
    return results

# === Main ===

if __name__ == "__main__":
    input_path = "data/gbif_threatened_species_raw.csv"
    output_path = "data/gbif_threatened_species.csv"

    if not os.path.exists(input_path):
        print(f"❌ Raw file not found at {input_path}")
        exit()

    df = pd.read_csv(input_path)

    missing = df["commonName"].isna()
    missing_names = df.loc[missing, "scientificName"].dropna().unique()
    print(f"🔍 Fetching common names for {len(missing_names)} unique scientific names...")

    name_map = enrich_common_names(missing_names)
    df.loc[missing, "commonName"] = df.loc[missing, "scientificName"].map(name_map)

    df.to_csv(output_path, index=False)
    print(f"\n✅ Enriched data saved to {output_path}")
    print(f"🔢 Total records: {len(df)}")
