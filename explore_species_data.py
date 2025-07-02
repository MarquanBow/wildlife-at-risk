import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
os.makedirs("data/plots", exist_ok=True)
df = pd.read_csv("data/gbif_threatened_species.csv")

# Plot A: Top 20 Countries
print("Plotting by country...")
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="country", order=df["country"].value_counts().index[:20], palette="viridis")
plt.xticks(rotation=45)
plt.title("Top 20 Countries by Species Observations")
plt.tight_layout()
plt.savefig("data/plots/species_per_country.png")
plt.close()
print("✅ Saved country plot")

# Plot B: Top 10 Species Classes
print("Plotting by class...")
class_counts = df["class"].value_counts().dropna().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=class_counts.values, y=class_counts.index, palette="mako")
plt.title("Top 10 Species Classes")
plt.tight_layout()
plt.savefig("data/plots/species_per_class.png")
plt.close()
print("✅ Saved class plot")
