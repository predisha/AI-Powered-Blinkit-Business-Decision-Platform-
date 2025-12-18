import streamlit as st
import pandas as pd

st.set_page_config(page_title="Blinkit Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return {
        "customers": pd.read_excel("Blinkit.xlsx", sheet_name="blinkit_customers"),
        "marketing": pd.read_excel("Blinkit.xlsx", sheet_name="blinkit_marketing_performance"),
        "feedback": pd.read_excel("Blinkit.xlsx", sheet_name="blinkit_customer_feedback"),
        "orders": pd.read_excel("Blinkit.xlsx", sheet_name="blinkit_orders")
    }

data = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Marketing Analysis", "Customer Feedback", "Delay Prediction"]
)

# ---------------- OVERVIEW PAGE ----------------
if page == "Overview":
    st.title("📊 Blinkit Business Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", len(data["customers"]))
    col2.metric("Total Orders", len(data["orders"]))
    col3.metric("Total Feedbacks", len(data["feedback"]))

    st.subheader("Orders Preview")
    st.dataframe(data["orders"].head())

# ---------------- MARKETING ANALYSIS ----------------
elif page == "Marketing Analysis":
    st.title("📈 Marketing Performance Analysis")

    marketing = data["marketing"]

    st.subheader("Marketing Dataset Preview")
    st.dataframe(marketing.head())

    required_cols = {"impressions", "clicks", "conversions", "channel"}

    if required_cols.issubset(marketing.columns):

        # Calculate metrics
        marketing["CTR (%)"] = (marketing["clicks"] / marketing["impressions"]) * 100
        marketing["Conversion Rate (%)"] = (marketing["conversions"] / marketing["clicks"]) * 100

        st.subheader("📊 Channel-wise Performance")
        channel_summary = marketing.groupby("channel")[[
            "impressions", "clicks", "conversions"
        ]].sum()

        st.dataframe(channel_summary)

        st.subheader("📈 Clicks by Channel")
        st.bar_chart(channel_summary["clicks"])

        st.subheader("📉 Average Conversion Rate by Channel")
        st.bar_chart(
            marketing.groupby("channel")["Conversion Rate (%)"].mean()
        )

    else:
        st.error("Required marketing columns missing.")

# ---------------- CUSTOMER FEEDBACK ----------------
elif page == "Customer Feedback":
    st.title("📢 Customer Feedback Analysis")

    feedback = data["feedback"]

    st.subheader("Dataset Preview")
    st.dataframe(feedback.head())

    text_col = "feedback_text"
    st.success(f"Using feedback column: {text_col}")

    st.subheader("Sample Feedbacks")
    st.dataframe(feedback[[text_col]].dropna().head(10))

    if "sentiment" in feedback.columns:
        st.subheader("Sentiment Distribution")
        st.bar_chart(feedback["sentiment"].value_counts())

# ---------------- DELAY PREDICTION ----------------
elif page == "Delay Prediction":
    st.title("⏱️ Order Delay Prediction")

    st.info("This is a rule-based delay indicator.")

    orders = data["orders"]

    if {"promised_delivery_time", "actual_delivery_time"}.issubset(orders.columns):

        orders["promised_delivery_time"] = pd.to_datetime(orders["promised_delivery_time"])
        orders["actual_delivery_time"] = pd.to_datetime(orders["actual_delivery_time"])

        orders["delay_minutes"] = (
            orders["actual_delivery_time"] - orders["promised_delivery_time"]
        ).dt.total_seconds() / 60

        orders["delay_status"] = orders["delay_minutes"].apply(
            lambda x: "Delayed" if x > 0 else "On Time"
        )

        st.subheader("Delay Prediction Preview")
        st.dataframe(
            orders[[
                "order_id",
                "promised_delivery_time",
                "actual_delivery_time",
                "delay_minutes",
                "delay_status"
            ]].head()
        )

        st.subheader("📊 Delay Status Distribution")
        st.bar_chart(orders["delay_status"].value_counts())

    else:
        st.error("Delivery time columns missing.")








