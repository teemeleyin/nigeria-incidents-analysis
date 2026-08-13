import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Nigeria Incidents Dashboard",
    layout="wide"
)

# Title
st.title("Nigeria Incidents and Violence Analysis Dashboard")
st.write(
    "This dashboard presents an analysis of incidents and fatalities in Nigeria."
)

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("incidents_updated.csv")

    df["Start date"] = pd.to_datetime(
        df["Start date"],
        format="%Y-%m-%d"
    )

    df["End date"] = pd.to_datetime(
        df["End date"],
        format="%Y-%m-%d"
    )

    df["Year"] = df["Start date"].dt.year
    df["Month"] = df["Start date"].dt.month_name()

    return df


df = load_data()

# Sidebar filter
st.sidebar.header("Filter")

# Sidebar filter
st.sidebar.header("Filter")

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(df["Year"].dropna().unique().tolist())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["Month"].dropna().unique().tolist())
)

if year != "All":
    df = df[df["Year"] == year]

if month != "All":
    df = df[df["Month"] == month]
# KPI section
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Incidents",
    len(df)
)

col2.metric(
    "Total Deaths",
    int(df["Number of deaths"].sum())
)

col3.metric(
    "Average Deaths per Incident",
    round(df["Number of deaths"].mean(), 2)
)

# Dataset preview
st.subheader("Dataset Preview")

st.dataframe(df.head(10))

# Incidents by Year
st.subheader("Number of Incidents by Year")

incidents_per_year = df["Year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))

incidents_per_year.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Incidents")
ax.set_title("Number of Incidents by Year")

st.pyplot(fig)

# Deaths by Year
st.subheader("Total Deaths by Year")
# Incidents by Month
st.subheader("Number of Incidents by Month")

incidents_per_month = df["Month"].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))

incidents_per_month.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Number of Incidents")
ax.set_title("Number of Incidents by Month")
plt.xticks(rotation=45)

st.pyplot(fig)
# Deaths by Month
st.subheader("Total Deaths by Month")

deaths_per_month = df.groupby("Month")["Number of deaths"].sum()

fig, ax = plt.subplots(figsize=(10, 5))

deaths_per_month.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Total Deaths")
ax.set_title("Total Deaths by Month")
plt.xticks(rotation=45)

st.pyplot(fig)

deaths_per_year = df.groupby("Year")["Number of deaths"].sum()

fig, ax = plt.subplots(figsize=(10, 5))

deaths_per_year.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Year")
ax.set_ylabel("Total Deaths")
ax.set_title("Total Deaths by Year")

st.pyplot(fig)

# Top 10 deadliest incidents
st.subheader("Top 10 Deadliest Incidents")

top10 = df.nlargest(10, "Number of deaths")

st.dataframe(
    top10[["Title", "Start date", "Number of deaths"]]
)

# Footer
st.markdown("---")

st.write(
    "Python Data Analysis Project — Nigeria Incidents Dataset"
)
# Download filtered data
st.subheader("Download Filtered Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="filtered_incidents.csv",
    mime="text/csv"
)