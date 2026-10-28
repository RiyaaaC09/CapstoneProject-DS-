import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Population Segmentation",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/powerbi_members.csv"
)

# =====================================================
# TITLE
# =====================================================

st.title("🧩 Population Segmentation")

st.markdown("""
Population segments identified through
clustering analysis.
""")

# =====================================================
# CLUSTER COUNTS
# =====================================================

st.subheader(
    "Population Segment Distribution"
)

cluster_counts = (
    df["Cluster_Name"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Cluster",
    "Members"
]

fig_cluster = px.pie(
    cluster_counts,
    values="Members",
    names="Cluster",
    title="Cluster Distribution"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

# =====================================================
# CLUSTER CHARACTERISTICS
# =====================================================

st.subheader(
    "Cluster Characteristics"
)

cluster_summary = (
    df.groupby("Cluster_Name")
    .agg({
        "Age": "mean",
        "BMI": "mean",
        "Glucose": "mean"
    })
    .round(2)
)

st.dataframe(cluster_summary)

# =====================================================
# AVERAGE BMI BY CLUSTER
# =====================================================

st.subheader(
    "Average BMI by Segment"
)

bmi_cluster = (
    df.groupby("Cluster_Name")["BMI"]
    .mean()
    .reset_index()
)

fig_bmi = px.bar(
    bmi_cluster,
    x="Cluster_Name",
    y="BMI",
    title="Average BMI by Segment"
)

st.plotly_chart(
    fig_bmi,
    use_container_width=True
)

# =====================================================
# AVERAGE GLUCOSE BY CLUSTER
# =====================================================

st.subheader(
    "Average Glucose by Segment"
)

glucose_cluster = (
    df.groupby("Cluster_Name")["Glucose"]
    .mean()
    .reset_index()
)

fig_glucose = px.bar(
    glucose_cluster,
    x="Cluster_Name",
    y="Glucose",
    title="Average Glucose by Segment"
)

st.plotly_chart(
    fig_glucose,
    use_container_width=True
)

# =====================================================
# MEMBER EXPLORER
# =====================================================

st.subheader(
    "Segment Member Sample"
)

selected_cluster = st.selectbox(
    "Select Cluster",
    df["Cluster_Name"]
    .dropna()
    .unique()
)

filtered_df = df[
    df["Cluster_Name"] == selected_cluster
]

st.dataframe(
    filtered_df[
        [
            "Member_ID",
            "Age",
            "BMI",
            "Glucose",
            "Smoking_Status"
        ]
    ].head(20)
)