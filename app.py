import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# -------------------------------
# CUSTOM STYLE (🔥 PREMIUM LOOK)
# -------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }

    /* Text color */
    .css-18e3th9 {
        color: white;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #111827;
    }

    /* Metric cards */
    .stMetric {
        color: white;
    }

    /* Table text */
    .stDataFrame {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Stock Analysis Dashboard")
st.markdown("#### 🚀 Advanced Stock Insights (All Tasks)")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(r"D:\Data science\Stock Analysis\all_stock_data.csv")
sector_df = pd.read_csv(r"D:\Data science\Stock Analysis\sector_data.csv")

df = df.sort_values(by=["Ticker", "date"])
df["Daily Return"] = df.groupby("Ticker")["close"].pct_change()

# -------------------------------
# KPI CARDS (🔥 IMPRESSIVE)
# -------------------------------
total_stocks = df["Ticker"].nunique()
avg_price = df["close"].mean()
avg_volume = df["volume"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("📌 Total Stocks", total_stocks)
col2.metric("💰 Avg Price", f"{avg_price:.2f}")
col3.metric("📦 Avg Volume", f"{avg_volume:.0f}")

st.divider()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("📌 Navigation")
task = st.sidebar.radio(
    "Select Analysis",
    ["Volatility", "Cumulative", "Sector", "Correlation", "Monthly"]
)

# -------------------------------
# VOLATILITY
# -------------------------------
if task == "Volatility":
    st.subheader("📈 Top 10 Most Volatile Stocks")

    volatility = df.groupby("Ticker")["Daily Return"].std().reset_index()
    volatility.columns = ["Ticker", "Volatility"]

    top_volatile = volatility.sort_values(by="Volatility", ascending=False).head(10)

    col1, col2 = st.columns([1,2])

    col1.dataframe(top_volatile)

    fig, ax = plt.subplots()
    top_volatile.plot(x="Ticker", y="Volatility", kind="bar", ax=ax)
    ax.set_title("Volatility")
    col2.pyplot(fig)

# -------------------------------
# CUMULATIVE
# -------------------------------
elif task == "Cumulative":
    st.subheader("📊 Cumulative Return (Top 5 Stocks)")

    returns = df.groupby("Ticker").apply(
        lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
    )

    returns_df = returns.reset_index()
    returns_df.columns = ["Ticker", "Yearly Return"]

    top5 = returns_df.sort_values(by="Yearly Return", ascending=False).head(5)["Ticker"]

    top5_df = df[df["Ticker"].isin(top5)].copy()
    top5_df["Cumulative Return"] = top5_df.groupby("Ticker")["Daily Return"].cumsum()

    fig, ax = plt.subplots()

    for ticker in top5:
        data = top5_df[top5_df["Ticker"] == ticker]
        ax.plot(range(len(data)), data["Cumulative Return"], label=ticker)

    ax.legend()
    ax.set_title("Cumulative Return Trend")
    st.pyplot(fig)

# -------------------------------
# SECTOR
# -------------------------------
elif task == "Sector":
    st.subheader("🏭 Sector Performance")

    sector_perf = df.groupby("Ticker").apply(
        lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
    ).reset_index()

    sector_perf.columns = ["Ticker", "Yearly Return"]

    sector_perf = sector_perf.merge(sector_df, on="Ticker", how="left")

    sector_avg = sector_perf.groupby("Sector")["Yearly Return"].mean().reset_index()

    col1, col2 = st.columns([1,2])

    col1.dataframe(sector_avg)

    fig, ax = plt.subplots()
    sector_avg.plot(x="Sector", y="Yearly Return", kind="bar", ax=ax)
    ax.set_title("Sector-wise Performance")
    col2.pyplot(fig)

# -------------------------------
# CORRELATION
# -------------------------------
elif task == "Correlation":
    st.subheader("🔗 Correlation Heatmap")

    pivot_df = df.pivot(index="date", columns="Ticker", values="close")

    returns = df.groupby("Ticker").apply(
        lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
    )

    top_stocks = returns.sort_values(ascending=False).head(10).index
    pivot_df = pivot_df[top_stocks]

    corr = pivot_df.corr()

    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(corr, cmap="coolwarm", ax=ax)

    st.pyplot(fig)

# -------------------------------
# MONTHLY
# -------------------------------
elif task == "Monthly":
    st.subheader("📅 Monthly Gainers & Losers")

    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")

    monthly = df.groupby(["month", "Ticker"]).apply(
        lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
    ).reset_index()

    monthly.columns = ["Month", "Ticker", "Monthly Return"]

    month = st.selectbox("Select Month", monthly["Month"].astype(str).unique())

    data = monthly[monthly["Month"].astype(str) == month]

    top5 = data.sort_values(by="Monthly Return", ascending=False).head(5)
    bottom5 = data.sort_values(by="Monthly Return", ascending=True).head(5)

    col1, col2 = st.columns(2)

    col1.write("Top 5 Gainers")
    col1.dataframe(top5)

    col2.write("Top 5 Losers")
    col2.dataframe(bottom5)

    fig, ax = plt.subplots()
    pd.concat([top5, bottom5]).plot(x="Ticker", y="Monthly Return", kind="bar", ax=ax)
    st.pyplot(fig)