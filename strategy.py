import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Population Strategy Dashboard",
    layout="wide"
)

# =====================================================
# LOAD RECOMMENDATIONS
# =====================================================

recommendation_df = pd.read_csv(
    "data/member_recommendations.csv"
)

# =====================================================
# TITLE
# =====================================================

st.title("📈 Population Strategy Dashboard")

st.markdown("""
Executive view of intervention priorities,
recommendations, and member outreach strategy.
""")

# =====================================================
# KPI SECTION
# =====================================================

total_members = len(recommendation_df)

high_risk_members = len(
    recommendation_df[
        recommendation_df[
            "Risk_Probability"
        ] >= 0.80
    ]
)

avg_risk = round(
    recommendation_df[
        "Risk_Probability"
    ].mean() * 100,
    2
)

clusters = recommendation_df[
    "Cluster_Name"
].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Members With Recommendations",
        total_members
    )

with col2:
    st.metric(
        "High-Risk Members",
        high_risk_members
    )

with col3:
    st.metric(
        "Average Risk %",
        avg_risk
    )

with col4:
    st.metric(
        "Population Segments",
        clusters
    )

# =====================================================
# RISK CATEGORY DISTRIBUTION
# =====================================================

st.subheader(
    "Risk Category Distribution"
)

risk_counts = (
    recommendation_df["Risk_Category"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Category",
    "Members"
]

fig_risk = px.bar(
    risk_counts,
    x="Risk Category",
    y="Members",
    color="Risk Category",
    title="Members by Risk Category"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# =====================================================
# SEGMENT DISTRIBUTION
# =====================================================

st.subheader(
    "Population Segment Distribution"
)

cluster_counts = (
    recommendation_df["Cluster_Name"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Segment",
    "Members"
]

fig_cluster = px.pie(
    cluster_counts,
    values="Members",
    names="Segment",
    title="Population Segments"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

# =====================================================
# MEMBER SEARCH
# =====================================================

st.subheader(
    "Recommendation Repository"
)

selected_member = st.selectbox(
    "Select Member",
    recommendation_df["Member_ID"]
)

member_data = recommendation_df[
    recommendation_df["Member_ID"]
    == selected_member
].iloc[0]

st.markdown("### Stored AI Recommendation")

st.text_area(
    "AI Recommendation",
    member_data["AI_Recommendation"],
    height=350
)

# =====================================================
# TOP HIGH-RISK MEMBERS
# =====================================================

st.subheader(
    "Top High-Risk Members"
)

top_high_risk = (
    recommendation_df
    .sort_values(
        "Risk_Probability",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_high_risk[
        [
            "Member_ID",
            "Risk_Probability",
            "Risk_Category",
            "Cluster_Name"
        ]
    ]
)

# =====================================================
# EXECUTIVE STRATEGY SUMMARY
# =====================================================

st.subheader(
    "Executive Recommendations"
)

st.success("""
1. Prioritize High-Risk Chronic Members
   for proactive care management.

2. Increase enrollment in wellness
   and diabetes prevention programs.

3. Expand preventive screening
   participation among high-risk members.

4. Strengthen outreach and follow-up
   for members with elevated risk scores.

5. Focus care coordination resources
   on the highest-risk populations.
""")