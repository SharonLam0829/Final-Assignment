import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Load the data
df = pd.read_csv("data/Electric_Vehicle_Population_Data.csv")

# Set page configuration
st.set_page_config(page_title="Electric Vehicle Population", page_icon=":car:", layout="wide")

# Sidebar
st.sidebar.title("Electric Vehicle Population")
st.sidebar.image("image/electric_car.jpg", use_column_width=True)
vehicle_brands = df['Make'].unique()
selected_brand = st.sidebar.selectbox("Select Vehicle Brand", vehicle_brands)


# Filter data based on selected brand
filtered_df = df[df['Make'] == selected_brand]

# Sidebar - Model selection
vehicle_models = filtered_df['Model'].unique()
selected_model = st.sidebar.selectbox("Select Vehicle Model", vehicle_models)


# Filter data based on selected model
filtered_df = filtered_df[filtered_df['Model'] == selected_model]

# Display image for selected brand and model
image_path = f"image/{selected_brand}_{selected_model}.jpg"
try:
    image = Image.open(image_path)
    st.image(image, caption=f"{selected_brand} {selected_model}", use_column_width=True)
except FileNotFoundError:
    st.write(f"Image for {selected_brand} {selected_model} not found.")

# Display scatter plot
st.header(f"Electric Vehicle Population - {selected_brand} {selected_model}")
st.subheader("Scatter Plot of Electric Vehicle Data")
selected_x_var = st.selectbox("Select X Variable", filtered_df.columns)
selected_y_var = st.selectbox("Select Y Variable", filtered_df.columns)
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x=selected_x_var, y=selected_y_var)
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title(f"{selected_brand} {selected_model} Electric Vehicle Population")
st.pyplot(fig)

# Display table of filtered data
st.subheader("Filtered Vehicle")
st.dataframe(filtered_df)

# Display descriptive statistics
st.subheader("Descriptive Statistics")
st.dataframe(filtered_df.describe())

# Display histogram of vehicle years
st.subheader("Histogram of Vehicle Years")
sns.histplot(data=filtered_df, x='Model Year', bins=10, kde=True)
plt.xlabel("Model Year")
plt.ylabel("Count")
st.pyplot()

# Display map of vehicle locations
st.subheader("Map of Vehicle Locations")
if 'LATITUDE' in filtered_df.columns and 'LONGITUDE' in filtered_df.columns:
    st.map(filtered_df[['LATITUDE', 'LONGITUDE']])
else:
    st.write("Latitude and Longitude columns not found in the dataset.")

# Display raw data
st.subheader("Raw Data")
st.dataframe(df)
