import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the data
df_path = "data/gbif_threatened_species.csv"
if not os.path.exists(df_path):
    raise FileNotFoundError(f"CSV not found at {df_path}")

df = pd.read_csv(df_path)

# Basic inspection
print("🔍 Dataset preview:")
print(df.head(), "\n")
print(f"Shape: {df.shape}")
print(f"Missing values:\n{df.isna().sum()}")

# Drop rows without species names or country
df.dropna(subset=["species", "country"], inplace=True)

# Fill missing threat status with 'Unknown'
df["threat_status"] = df["threat_status"].fillna("Unknown")

# =============================
# 🧮 Summary 1: Count per country
# =============================
country_counts = df["country"].value_counts()
print("\n🌍 Threatened species records by country:")
print(country_counts)

# =============================
# 📚 Summary 2: Top 10 species
# =============================
top_species = df["species"].value_counts().head(10)
print("\n🦎 Top 10 most commonly recorded threatened species:")
print(top_species)

# =============================
# 📊 Summary 3: Top taxonomic classes
# =============================
top_classes = df["class"].value_counts().head(10)
print("\n🧬 Top 10 classes (taxonomic groups):")
print(top_classes)

# =============================
# 📈 Visualization
# =============================
sns.set(style="whitegrid")

# Threatened records per country
plt.figure(figsize=(8, 5))
sns.barplot(x=country_counts.index, y=country_counts.values, palette="muted")
plt.title("Threatened Species Records by Country")
plt.xlabel("Country")
plt.ylabel("Record Count")
plt.tight_layout()
plt.savefig("data/plots/species_by_country.png")
plt.close()

# Top 10 taxonomic classes
plt.figure(figsize=(10, 5))
sns.barplot(x=top_classes.index, y=top_classes.values, palette="viridis")
plt.title("Top 10 Threatened Species Classes")
plt.xticks(rotation=45)
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("data/plots/top_classes.png")
plt.close()

print("\n📊 Plots saved to data/plots/")
