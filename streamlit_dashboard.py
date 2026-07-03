# ============================================================
# SUBSCRIPTION TRAP DETECTOR DASHBOARD
# PROFESSIONAL VERSION
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Subscription Trap Detector",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar Background */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #374151;
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: white !important;
    font-weight: bold !important;
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 42px !important;
    font-weight: 700 !important;
}

/* Multiselect Boxes */
.stMultiSelect > div > div {
    background-color: #1f2937 !important;
    color: white !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #1f2937 !important;
    color: white !important;
}

/* Radio Buttons */
.stRadio label {
    color: white !important;
}

/* Headers */
h1, h2, h3, h4 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

subscription_df = pd.read_csv("cleaned_subscription_data.csv")
customer_features = pd.read_csv("customer_subscription_features.csv")

customer_features["risk"] = np.where(
    customer_features["overspending_flag"] == 1,
    "High",
    np.where(
        customer_features["isolation_forest_anomaly"] == 1,
        "Medium",
        "Low"
    )
)

st.title("📊 Subscription Trap Detector Dashboard")

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Overview","EDA","Anomalies","Zombie Subs","Customer View"]
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    subscription_df["gender"].unique(),
    default=subscription_df["gender"].unique()
)

selected_age = st.sidebar.multiselect(
    "Age Group",
    subscription_df["age"].unique(),
    default=subscription_df["age"].unique()
)

selected_category = st.sidebar.multiselect(
    "Category",
    subscription_df["category"].unique(),
    default=subscription_df["category"].unique()
)

filtered_df = subscription_df[
    (subscription_df["gender"].isin(selected_gender)) &
    (subscription_df["age"].isin(selected_age)) &
    (subscription_df["category"].isin(selected_category))
]

if page == "Overview":

    total_customers = filtered_df["customer"].nunique()
    total_spending = filtered_df["amount"].sum()
    anomalies = int(customer_features["isolation_forest_anomaly"].sum())
    overspending = int(customer_features["overspending_flag"].sum())

    colA,colB = st.columns(2)
    with colA:
        st.error(f"🚨 {anomalies:,} Anomalies Detected")
    with colB:
        st.success("✅ Pipeline Complete")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("👥 Total Customers", f"{total_customers:,}")
    c2.metric("💰 Total Spending", f"${total_spending:,.0f}")
    c3.metric("🚨 Anomalies", anomalies)
    c4.metric("⚠️ Overspending", overspending)

    monthly_spending = filtered_df.groupby("month")["amount"].sum().reset_index()

    fig = px.line(monthly_spending, x="month", y="amount", markers=True,
                  title="Monthly Subscription Spending")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    customer_features["spending_zone"] = pd.cut(
        customer_features["total_spending"],
        bins=3,
        labels=["Low","Normal","High"]
    )

    zone_counts = customer_features["spending_zone"].value_counts()

    fig2 = px.pie(
        values=zone_counts.values,
        names=zone_counts.index,
        hole=0.7,
        title="Spending Zones"
    )
    fig2.update_traces(textinfo="percent+label")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    a,b,c = st.columns(3)
    with a:
        st.subheader("👥 Gender Split")
        st.dataframe(filtered_df["gender"].value_counts())
    with b:
        st.subheader("📂 Category Split")
        st.dataframe(filtered_df["category"].value_counts())
    with c:
        st.subheader("🎂 Age Groups")
        st.dataframe(filtered_df["age"].value_counts())

elif page == "EDA":
    st.header("📊 Exploratory Data Analysis")

    category_counts = filtered_df["category"].value_counts()
    fig = px.bar(x=category_counts.index, y=category_counts.values,
                 title="Category Distribution")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    gender_counts = filtered_df["gender"].value_counts()
    fig2 = px.bar(x=gender_counts.index, y=gender_counts.values,
                  title="Gender Distribution")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Anomalies":
    st.header("🚨 Isolation Forest Anomalies")

    fig = px.scatter(
        customer_features,
        x="subscription_count",
        y="total_spending",
        color="isolation_forest_anomaly",
        hover_data=["customer"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        customer_features[customer_features["isolation_forest_anomaly"] == 1]
    )

elif page == "Zombie Subs":
    st.header("🧟 Zombie Subscriptions")
    st.dataframe(
        customer_features[customer_features["zombie_subscription"] == 1]
    )

elif page == "Customer View":
    customer_id = st.selectbox(
        "Select Customer",
        customer_features["customer"]
    )
    st.dataframe(
        customer_features[customer_features["customer"] == customer_id]
    )

st.markdown("---")
st.header("⚠️ Customer Risk Table")

# Show only High and Medium Risk Customers

risk_table = customer_features[
    customer_features["risk"] != "Low"
][
    [
        "customer",
        "total_spending",
        "average_spending",
        "subscription_count",
        "risk"
    ]
]

st.dataframe(
    risk_table,
    use_container_width=True,
    height=500
)

st.info(
    f"Showing {len(risk_table):,} High and Medium Risk Customers"
)
