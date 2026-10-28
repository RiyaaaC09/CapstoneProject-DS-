import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Population Health Overview",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

members_df = pd.read_csv(
    "data/powerbi_members.csv"
)

risk_df = pd.read_csv(
    "data/risk_scores.csv"
)

# =====================================================
# MERGE DATA
# =====================================================

df = members_df.merge(
    risk_df,
    on="Member_ID",
    how="left"
)

# =====================================================
# FIX DUPLICATE COLUMN NAMES
# =====================================================

if "Risk_Category_x" in df.columns:
    df = df.rename(
        columns={
            "Risk_Category_x": "Risk_Category"
        }
    )

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏠 Population Health Overview")

st.markdown(
    "Executive summary of population health metrics."
)

# =====================================================
# KPI METRICS
# =====================================================

total_members = len(df)

avg_age = round(
    df["Age"].mean(),
    1
)

avg_bmi = round(
    df["BMI"].mean(),
    1
)

avg_risk = round(
    df["Risk_Probability"].mean() * 100,
    1
)

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Members",
        f"{total_members:,}"
    )

with col2:
    st.metric(
        "Average Age",
        avg_age
    )

with col3:
    st.metric(
        "Average BMI",
        avg_bmi
    )

with col4:
    st.metric(
        "Average Risk %",
        f"{avg_risk}%"
    )

# =====================================================
# HIGH RISK COUNTS
# =====================================================

high_risk_count = len(
    df[
        df["Risk_Probability"] >= 0.80
    ]
)

very_high_risk_count = len(
    df[
        df["Risk_Probability"] >= 0.90
    ]
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "High Risk Members",
        high_risk_count
    )

with col2:
    st.metric(
        "Very High Risk Members",
        very_high_risk_count
    )

# =====================================================
# RISK CATEGORY DISTRIBUTION
# =====================================================

st.subheader(
    "Risk Category Distribution"
)

risk_counts = (
    df["Risk_Category"]
    .fillna("Unknown")
    .value_counts()
)

st.bar_chart(
    risk_counts
)

# =====================================================
# CLUSTER DISTRIBUTION
# =====================================================

st.subheader(
    "Population Segmentation"
)

cluster_counts = (
    df["Cluster_Name"]
    .fillna("Unknown")
    .value_counts()
)

st.bar_chart(
    cluster_counts
)

# =====================================================
# QUICK DATA PREVIEW
# =====================================================

st.subheader(
    "Sample Member Data"
)

preview_cols = [
    "Member_ID",
    "Age",
    "BMI",
    "Glucose",
    "Smoking_Status",
    "Cluster_Name",
    "Risk_Category",
    "Risk_Probability"
]

available_cols = [
    col for col in preview_cols
    if col in df.columns
]

st.dataframe(
    df[available_cols].head(10)
)

# =====================================================
# FOOTER
# =====================================================

st.info(
    "Use the sidebar to navigate through Analytics, Segmentation, Prediction, AI Health Advisor, and Strategy dashboards."
)