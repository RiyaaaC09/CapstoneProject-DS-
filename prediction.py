import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Risk Prediction Dashboard",
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

# Fix risk category naming

if "Risk_Category_x" in df.columns:
    df = df.rename(
        columns={
            "Risk_Category_x": "Risk_Category"
        }
    )

# =====================================================
# TITLE
# =====================================================

st.title("🤖 Risk Prediction Dashboard")

st.markdown("""
Machine Learning based population health
risk prediction and member risk scoring.
""")

# =====================================================
# KPI SECTION
# =====================================================

avg_risk = round(
    df["Risk_Probability"].mean() * 100,
    2
)

highest_risk = round(
    df["Risk_Probability"].max() * 100,
    2
)

high_risk_count = len(
    df[df["Risk_Probability"] >= 0.80]
)

very_high_risk_count = len(
    df[df["Risk_Probability"] >= 0.90]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Risk %",
        avg_risk
    )

with col2:
    st.metric(
        "Highest Risk %",
        highest_risk
    )

with col3:
    st.metric(
        "High Risk Members",
        high_risk_count
    )

with col4:
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
# RISK SCORE DISTRIBUTION
# =====================================================

st.subheader(
    "Risk Probability Distribution"
)

fig_probability = px.histogram(
    df,
    x="Risk_Probability",
    nbins=25,
    title="Risk Probability Distribution"
)

st.plotly_chart(
    fig_probability,
    use_container_width=True
)

# =====================================================
# TOP HIGH-RISK MEMBERS
# =====================================================

st.subheader(
    "Top 20 Highest-Risk Members"
)

top_members = (
    df.sort_values(
        "Risk_Probability",
        ascending=False
    )
    .head(20)
)

display_cols = [
    "Member_ID",
    "Age",
    "BMI",
    "Glucose",
    "Risk_Category",
    "Risk_Probability"
]

available_cols = [
    col for col in display_cols
    if col in top_members.columns
]

st.dataframe(
    top_members[available_cols]
)

# =====================================================
# AGE VS RISK
# =====================================================

st.subheader(
    "Age vs Risk Probability"
)

fig_age_risk = px.scatter(
    df,
    x="Age",
    y="Risk_Probability",
    color="Risk_Category",
    title="Age vs Risk Probability"
)

st.plotly_chart(
    fig_age_risk,
    use_container_width=True
)

# =====================================================
# BMI VS RISK
# =====================================================

st.subheader(
    "BMI vs Risk Probability"
)

fig_bmi_risk = px.scatter(
    df,
    x="BMI",
    y="Risk_Probability",
    color="Risk_Category",
    title="BMI vs Risk Probability"
)

st.plotly_chart(
    fig_bmi_risk,
    use_container_width=True
)

# =====================================================
# MODEL PERFORMANCE SECTION
# =====================================================

st.subheader(
    "Model Performance Comparison"
)

performance_df = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting",
        "Neural Network"
    ],
    "Accuracy": [
        0.618,
        0.815,
        0.845,
        0.885,
        0.784
    ],
    "Precision": [
        0.160,
        0.278,
        0.293,
        0.424,
        0.269
    ],
    "Recall": [
        0.628,
        0.488,
        0.353,
        0.295,
        0.628
    ],
    "F1": [
        0.254,
        0.354,
        0.320,
        0.348,
        0.376
    ],
    "ROC_AUC": [
        0.655,
        0.786,
        0.736,
        0.793,
        0.805
    ]
})

# =====================================================
# PERFORMANCE TABLE
# =====================================================

st.dataframe(
    performance_df,
    use_container_width=True
)

# =====================================================
# MODEL SELECTION KPIs
# =====================================================

st.subheader(
    "Selected Model Summary"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Primary Metric",
        "Recall"
    )

with col2:
    st.metric(
        "Selected Model",
        "Neural Network"
    )

with col3:
    st.metric(
        "Recall",
        "62.8%"
    )

with col4:
    st.metric(
        "ROC-AUC",
        "80.5%"
    )

# =====================================================
# RECALL COMPARISON
# =====================================================

st.subheader(
    "Recall Comparison Across Models"
)

fig_recall = px.bar(
    performance_df,
    x="Model",
    y="Recall",
    color="Recall",
    title="Recall Comparison"
)

st.plotly_chart(
    fig_recall,
    use_container_width=True
)

# =====================================================
# ROC AUC COMPARISON
# =====================================================

st.subheader(
    "ROC-AUC Comparison Across Models"
)

fig_roc = px.bar(
    performance_df,
    x="Model",
    y="ROC_AUC",
    color="ROC_AUC",
    title="ROC-AUC Comparison"
)

st.plotly_chart(
    fig_roc,
    use_container_width=True
)

# =====================================================
# ACCURACY COMPARISON
# =====================================================

st.subheader(
    "Accuracy Comparison Across Models"
)

fig_accuracy = px.bar(
    performance_df,
    x="Model",
    y="Accuracy",
    color="Accuracy",
    title="Accuracy Comparison"
)

st.plotly_chart(
    fig_accuracy,
    use_container_width=True
)

# =====================================================
# MODEL SELECTION EXPLANATION
# =====================================================

st.success("""
### Model Selection Justification

Healthcare risk prediction focuses on identifying members
who may develop chronic disease within the next 12 months.

For this use case, **Recall** was selected as the primary
evaluation metric because:

• A False Negative means a high-risk member is missed.

• Missing a high-risk member can delay preventive care,
  wellness enrollment, and care-management intervention.

• Identifying as many at-risk members as possible is more
  important than maximizing overall accuracy.

### Neural Network Performance

✅ Recall = 62.8% (Highest)

✅ ROC-AUC = 80.5% (Highest)

✅ F1 Score = 37.6% (Highest)

Because the Neural Network achieved the strongest
performance on the most clinically important metrics,
it was selected as the final model.

The risk probabilities displayed throughout this platform
and used by the AI Recommendation Engine were generated
using the Neural Network model.
""")