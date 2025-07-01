import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("📦 Loading data...")
df = pd.read_csv("data/species.csv")
print(f"✅ Loaded {len(df)} records")

os.makedirs("data/plots", exist_ok=True)

# 1. Plot top 20 countries
print("📊 Generating bar plot by country...")
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="country", order=df["country"].value_counts().index[:20], palette="viridis")
plt.xticks(rotation=45)
plt.title("Top 20 Countries by Species Count")
plt.tight_layout()
plt.savefig("data/plots/species_per_country.png")
plt.close()

# 2. Plot top 10 species classes
print("📊 Generating bar plot by class...")
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="class", order=df["class"].value_counts().index[:10], palette="magma")
plt.xticks(rotation=45)
plt.title("Top 10 Species Classes")
plt.tight_layout()
plt.savefig("data/plots/species_per_class.png")
plt.close()
