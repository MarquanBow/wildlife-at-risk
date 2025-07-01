# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🌿 Wildlife at Risk — Species Observations")

# Load data
df = pd.read_csv("data/gbif_threatened_species.csv")

# Sidebar filters
countries = df['country'].dropna().unique()
selected_country = st.sidebar.selectbox("Select a country", sorted(countries))

# Filter by selected country
filtered_df = df[df['country'] == selected_country]

st.markdown(f"### Showing data for **{selected_country}**")
st.write(f"🔢 Total records: {len(filtered_df)}")
st.write(f"📚 Unique species: {filtered_df['species'].nunique()}")
st.write(f"📊 Unique classes: {filtered_df['class'].nunique()}")

# Bar plot of species classes
st.markdown("#### Top Species Classes")
top_classes = filtered_df['class'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_classes.values, y=top_classes.index, palette="viridis", ax=ax)
st.pyplot(fig)
