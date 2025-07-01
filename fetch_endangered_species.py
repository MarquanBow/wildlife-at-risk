from pygbif import occurrences
import pandas as pd
import time

# List of ISO 2-letter country codes
countries = ["BR", "IN", "ID"]

# Store all records
records = []

# How many records per country to fetch (max per request = 300)
RECORD_LIMIT = 200

print("🔍 Fetching GBIF threatened species data...\n")

for country in countries:
    print(f"🌎 Country: {country}")
    try:
        results = occurrences.search(
            country=country,
            threatened=True,
            limit=RECORD_LIMIT
        )["results"]

        for r in results:
            record = {
                "species": r.get("scientificName"),
                "common_name": r.get("vernacularName"),
                "threat_status": r.get("threatStatus"),
                "basis_of_record": r.get("basisOfRecord"),
                "event_date": r.get("eventDate"),
                "latitude": r.get("decimalLatitude"),
                "longitude": r.get("decimalLongitude"),
                "kingdom": r.get("kingdom"),
                "phylum": r.get("phylum"),
                "class": r.get("class"),
                "order": r.get("order"),
                "family": r.get("family"),
                "genus": r.get("genus"),
                "country": r.get("country")
            }
            records.append(record)

        print(f"✅ Retrieved {len(results)} records from {country}\n")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error for {country}: {e}")

# Convert to DataFrame
df = pd.DataFrame(records)

# Drop records with no species name
df = df.dropna(subset=["species"])

# Save to CSV
df.to_csv("data/gbif_threatened_species.csv", index=False)
print(f"📁 Saved {len(df)} records to data/gbif_threatened_species.csv")
