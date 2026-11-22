import streamlit as st
import pandas as pd

st.set_page_config(page_title="Seller Dashboard", layout="wide")

st.title("Seller Sales Dashboard") # Here I am putting the title of my dashboard

df = pd.read_excel("sellers.xlsx")

# Here I am creating a new column by combining the name and last name of each seller
df["VENDOR"] = df["NAME"] + " " + df["LASTNAME"]

st.sidebar.header("Filters") # Here I am adding the filters to the sidebar

# Here I am getting all the different regions from the dataset
regions = ["All"] + sorted(df["REGION"].dropna().unique().tolist())

# Here I am creating a dropdown menu so the user can select a region
selected_region = st.sidebar.selectbox("Select Region", regions)

# Here I am filtering the dataset depending on the region selected by the user
if selected_region == "All":
    filtered_df = df
else:
    filtered_df = df[df["REGION"] == selected_region]

# Here I am displaying the seller information in a table
st.subheader("Seller Information")

st.dataframe(filtered_df, use_container_width=True)

# Here I am creating a section to display the main sales metrics
st.subheader("Sales Overview")

# Here I am dividing the section into three columns to display the metrics
col1, col2, col3 = st.columns(3)

# Here I am calculating and displaying the total units sold
col1.metric("Units Sold", f'{filtered_df["SOLD UNITS"].sum():,.0f}')

# Here I am calculating and displaying the total sales
col2.metric("Total Sales", f'{filtered_df["TOTAL SALES"].sum():,.0f}')

# Here I am calculating the average sales
col3.metric(
    "Average Sales",
    f'{filtered_df["SALES AVERAGE"].mean():.3f}'
    if not filtered_df.empty else "0"
)

# Here I am creating the graphs to visualize the sales information
st.subheader("Sales Graphs")

# If the user selects All, the graphs will compare the different regions
if selected_region == "All":

    # Here I am grouping the data by region and calculating the sales metrics
    graph_data = df.groupby("REGION").agg({
        "SOLD UNITS": "sum",
        "TOTAL SALES": "sum",
        "SALES AVERAGE": "mean"
    })

    # Here I am displaying the units sold for each region
    st.write("Units Sold by Region")
    st.bar_chart(graph_data["SOLD UNITS"])

    # Here I am displaying the total sales for each region
    st.write("Total Sales by Region")
    st.bar_chart(graph_data["TOTAL SALES"])

    # Here I am displaying the average sales for each region
    st.write("Average Sales by Region")
    st.bar_chart(graph_data["SALES AVERAGE"])

# If the user selects a specific region, the graphs will compare its vendors
else:

    # Here I am grouping the data by vendor and calculating the sales metrics
    graph_data = filtered_df.groupby("VENDOR").agg({
        "SOLD UNITS": "sum",
        "TOTAL SALES": "sum",
        "SALES AVERAGE": "mean"
    })

    # Here I am displaying the units sold by each vendor
    st.write("Units Sold by Vendor")
    st.bar_chart(graph_data["SOLD UNITS"])

    # Here I am displaying the total sales by each vendor
    st.write("Total Sales by Vendor")
    st.bar_chart(graph_data["TOTAL SALES"])

    # Here I am displaying the average sales by each vendor
    st.write("Average Sales by Vendor")
    st.bar_chart(graph_data["SALES AVERAGE"])

# Here I am creating another section to display information about a specific vendor
st.subheader("Specific Vendor")

# Here I am getting the list of vendors from the filtered dataset
vendors = sorted(filtered_df["VENDOR"].dropna().unique().tolist())

# Here I am creating a dropdown menu to select a specific vendor
if vendors:

    selected_vendor = st.selectbox("Select a Vendor", vendors)

    # Here I am filtering the dataset to display only the selected vendor
    vendor_data = filtered_df[
        filtered_df["VENDOR"] == selected_vendor
    ]

    # Here I am displaying the information of the selected vendor in a table
    st.dataframe(vendor_data, use_container_width=True)

else:
    # This message appears if there are no vendors available for the selected region
    st.write("No vendors available for this region.")
