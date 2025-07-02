import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/gbif_threatened_species.csv")

df = load_data()

# Sidebar country filter
st.sidebar.title("Filters")
countries = sorted(df["country"].dropna().unique())
selected_country = st.sidebar.selectbox("Select a country", ["All"] + countries)

# Filter data
filtered_df = df if selected_country == "All" else df[df["country"] == selected_country]

# Plot: Species per class
st.subheader("Top Species Classes")
top_classes = filtered_df["class"].value_counts().dropna().head(10)
fig_class, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=top_classes.values, y=top_classes.index, ax=ax, palette="mako")
ax.set_title("Top 10 Species Classes")
st.pyplot(fig_class, use_container_width=True)

# Plot: Species per country (only for 'All')
if selected_country == "All":
    st.subheader("Top Countries by Species Observations")
    top_countries = df["country"].value_counts().head(20)
    fig_country, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax2, palette="viridis")
    ax2.set_title("Top 20 Countries by Observations")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig_country, use_container_width=True)

# Display species cards
st.subheader(f"Species in {selected_country}" if selected_country != "All" else "All Species")
for _, row in filtered_df.iterrows():
    with st.container():
        cols = st.columns([1, 3])
        if pd.notna(row["image_url"]):
            cols[0].image(row["image_url"], use_container_width=True)
        else:
            cols[0].empty()
        cols[1].markdown(f"**Common Name**: {row['common_name'] or 'Unknown'}")
        cols[1].markdown(f"**Scientific Name**: *{row['species'] or 'Unknown'}*")
        cols[1].markdown(f"**Class**: `{row['class'] or 'Unknown'}`")
        if pd.notna(row["event_date"]):
            cols[1].markdown(f"**Observed On**: {row['event_date'][:10]}")
