import streamlit as st
import pandas as pd

from rag.rag_engine import (
    generate_member_recommendation
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Member Explorer",
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

# Fix duplicate risk category column

if "Risk_Category_x" in df.columns:
    df = df.rename(
        columns={
            "Risk_Category_x": "Risk_Category"
        }
    )

# =====================================================
# PAGE TITLE
# =====================================================

st.title("👤 Member Explorer")

st.markdown("""
View member details, risk prediction,
population segment, and AI-generated
healthcare recommendations.
""")

# =====================================================
# MEMBER SELECTION
# =====================================================

member_id = st.selectbox(
    "Select Member",
    df["Member_ID"]
)

selected_member = df[
    df["Member_ID"] == member_id
].iloc[0]

# =====================================================
# MEMBER PROFILE
# =====================================================

st.subheader("Member Profile")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Age",
        selected_member["Age"]
    )

    st.metric(
        "BMI",
        selected_member["BMI"]
    )

with col2:

    st.metric(
        "Glucose",
        selected_member["Glucose"]
    )

    st.metric(
        "Smoking Status",
        selected_member["Smoking_Status"]
    )

with col3:

    st.metric(
        "Hypertension",
        selected_member[
            "Existing_Hypertension_Flag"
        ]
    )

    st.metric(
        "Cluster",
        selected_member[
            "Cluster_Name"
        ]
    )

# =====================================================
# RISK INFORMATION
# =====================================================

st.subheader("Risk Information")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Risk Category",
        selected_member["Risk_Category"]
    )

with col2:

    st.metric(
        "Risk Probability",
        round(
            selected_member[
                "Risk_Probability"
            ] * 100,
            2
        )
    )

# =====================================================
# GENERATE RECOMMENDATION
# =====================================================

st.subheader(
    "AI Recommendation Engine"
)

if st.button(
    "Generate Recommendation"
):

    with st.spinner(
        "Generating recommendation..."
    ):

        recommendation = (
            generate_member_recommendation(
                selected_member
            )
        )

    st.markdown(
        recommendation
    )