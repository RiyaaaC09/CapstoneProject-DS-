import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Population Analytics",
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

st.title("📊 Population Analytics")

st.markdown("""
Explore population health characteristics,
demographics, lifestyle risk factors,
and clinical indicators.
""")

# =====================================================
# AGE DISTRIBUTION
# =====================================================

st.subheader("Age Distribution")

fig_age = px.histogram(
    df,
    x="Age",
    nbins=20,
    title="Population Age Distribution"
)

st.plotly_chart(
    fig_age,
    use_container_width=True
)

# =====================================================
# BMI DISTRIBUTION
# =====================================================

st.subheader("BMI Distribution")

fig_bmi = px.histogram(
    df,
    x="BMI",
    nbins=20,
    title="BMI Distribution"
)

st.plotly_chart(
    fig_bmi,
    use_container_width=True
)

# =====================================================
# GLUCOSE DISTRIBUTION
# =====================================================

st.subheader("Glucose Distribution")

fig_glucose = px.histogram(
    df,
    x="Glucose",
    nbins=20,
    title="Glucose Distribution"
)

st.plotly_chart(
    fig_glucose,
    use_container_width=True
)

# =====================================================
# SMOKING STATUS
# =====================================================

st.subheader("Smoking Status")

smoking_counts = (
    df["Smoking_Status"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

smoking_counts.columns = [
    "Smoking_Status",
    "Count"
]

fig_smoking = px.pie(
    smoking_counts,
    values="Count",
    names="Smoking_Status",
    title="Smoking Status Distribution"
)

st.plotly_chart(
    fig_smoking,
    use_container_width=True
)

# =====================================================
# HYPERTENSION STATUS
# =====================================================

st.subheader("Hypertension Status")

bp_counts = (
    df["Existing_Hypertension_Flag"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

bp_counts.columns = [
    "Hypertension",
    "Count"
]

fig_bp = px.bar(
    bp_counts,
    x="Hypertension",
    y="Count",
    title="Hypertension Distribution"
)

st.plotly_chart(
    fig_bp,
    use_container_width=True
)

# =====================================================
# AGE VS BMI
# =====================================================

st.subheader("Age vs BMI")

fig_scatter = px.scatter(
    df,
    x="Age",
    y="BMI",
    color="Smoking_Status",
    title="Age vs BMI"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# =====================================================
# SUMMARY STATISTICS
# =====================================================

st.subheader("Summary Statistics")

summary_cols = [
    "Age",
    "BMI",
    "Glucose"
]

available_cols = [
    c for c in summary_cols
    if c in df.columns
]

st.dataframe(
    df[available_cols]
    .describe()
)

# =====================================================
# DATA SAMPLE
# =====================================================

st.subheader("Sample Records")

preview_cols = [
    "Member_ID",
    "Age",
    "BMI",
    "Glucose",
    "Smoking_Status",
    "Existing_Hypertension_Flag"
]

available_cols = [
    c for c in preview_cols
    if c in df.columns
]

st.dataframe(
    df[available_cols]
    .head(25)
)