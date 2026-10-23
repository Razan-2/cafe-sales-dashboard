import streamlit as st
import pandas as pd

df = pd.read_csv("clean_data.csv")

st.title("Cafe Sales Dashboard")

# Sidebar
st.sidebar.header("About the Dataset")
st.sidebar.write("Cafe sales data for 2023 from Kaggle. "
                 "Each row is one order with the item, quantity, price, "
                 "total spent, payment method and location.")

st.sidebar.header("Filters")

payment = st.sidebar.selectbox("Payment Method",
                               ["All"] + sorted(df["payment_method"].unique()))

min_total, max_total = st.sidebar.slider("Total Spent",
                                         float(df["total_spent"].min()),
                                         float(df["total_spent"].max()),
                                         (float(df["total_spent"].min()), float(df["total_spent"].max())))

items = st.sidebar.multiselect("Items",
                               sorted(df["item"].unique()),
                               default=sorted(df["item"].unique()))

# Apply filters
filtered = df[(df["total_spent"] >= min_total) &
              (df["total_spent"] <= max_total) &
              (df["item"].isin(items))]

if payment != "All":
    filtered = filtered[filtered["payment_method"] == payment]

# Data preview
st.header("Data Preview")
st.dataframe(filtered.head(20))

# Summary statistics
st.header("Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Orders", len(filtered))
col2.metric("Total Revenue", round(filtered["total_spent"].sum(), 2))
col3.metric("Average Order", round(filtered["total_spent"].mean(), 2))
st.write(filtered.describe())

# Visualizations
st.header("Visualizations")

st.subheader("Number of Orders per Item")
st.bar_chart(filtered["item"].value_counts())

st.subheader("Total Revenue per Item")
st.bar_chart(filtered.groupby("item")["total_spent"].sum())

st.subheader("Orders by Location")
st.bar_chart(filtered["location"].value_counts())

st.subheader("Quantity vs Total Spent")
st.scatter_chart(filtered, x="quantity", y="total_spent", color="item")

# Insights
st.header("Insights")
st.write("- Salad brings the highest revenue because it is the most expensive item.")
st.write("- All items have a similar number of orders.")
st.write("- Cash, Credit Card and Digital Wallet are used almost equally.")
st.write("- The payment method does not affect how much customers spend.")
st.write("- About 32% of payment methods and 40% of locations are Unknown.")
