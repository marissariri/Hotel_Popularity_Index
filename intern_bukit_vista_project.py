# Import necessary libraries
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


# load customer churn dataset
df = pd.read_csv("bukitvista_property.csv")
df.head()


import streamlit as st
# Streamlit App
st.title("Hotel Popularity Index")
st.sidebar.header("Customize Weights")

from sklearn.preprocessing import MinMaxScaler

# Normalize numerical features
scaler = MinMaxScaler()
df[["Price per Night (USD)", "Bedroom", "Bathroom"]] = scaler.fit_transform(
    df[["Price per Night (USD)", "Bedroom", "Bathroom"]]
)

# Assign weights
# Customize weights
weights = {
    "Price per Night (USD)": st.sidebar.slider("Weight for Price", 0.0, 1.0, 0.3),
    "Bedroom": st.sidebar.slider("Weight for Bedrooms", 0.0, 1.0, 0.2),
    "Bathroom": st.sidebar.slider("Weight for Bathrooms", 0.0, 1.0, 0.15),
}

# Ensure the weights sum to 1
total_weight = sum(weights.values())
if total_weight > 1.0:
    st.sidebar.error("Total weight should not exceed 1.0!")


# Calculate the popularity index
df["Popularity Index"] = (
    df["Price per Night (USD)"] * weights["Price per Night (USD)"] +
    df["Bedroom"] * weights["Bedroom"] +
    df["Bathroom"] * weights["Bathroom"]
)


# Rank the hotels
df["Rank"] = df["Popularity Index"].rank(ascending=False).astype(int)

# Sort by popularity index
df = df.sort_values(by="Popularity Index", ascending=False)

#df

# Display the DataFrame
st.subheader("Top Ranked Hotels")
st.write(df[["Rank", "Hotel Name", "Popularity Index"]])


# Plot the Popularity Index
st.subheader("Popularity Index Bar Chart")
fig, ax = plt.subplots()
df_sorted = df.sort_values(by="Popularity Index", ascending=True)
ax.barh(df_sorted["Hotel Name"], df_sorted["Popularity Index"], color="skyblue")
ax.set_xlabel("Popularity Index")
ax.set_ylabel("Hotel Name")
ax.set_title("Hotel Popularity Index")
st.pyplot(fig)


