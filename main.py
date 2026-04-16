import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt

folder_path = r"D:\Data science\Stock Analysis\data\New folder"

all_data = []


# STEP 1: READ YAML FILES

for file in os.listdir(folder_path):
    if file.endswith(".yaml"):
        file_path = os.path.join(folder_path, file)

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

            if isinstance(data, list):
                all_data.extend(data)

# -------------------------------
# STEP 2: CREATE DATAFRAME
# -------------------------------
df = pd.DataFrame(all_data)

print(df.head())
print("Total rows:", len(df))

# -------------------------------
# STEP 3: SAVE MASTER CSV
# -------------------------------
df.to_csv("all_stock_data.csv", index=False)


# STEP 4: CREATE SEPARATE CSV FILES
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

for ticker, data in df.groupby("Ticker"):
    file_path = os.path.join(output_folder, f"{ticker}.csv")
    data.to_csv(file_path, index=False)

print("Separate CSV files created!")

# -------------------------------
# STEP 5: CREATE DAILY RETURN (IMPORTANT FIX)
# -------------------------------
df = df.sort_values(by=["Ticker", "date"])

df["Daily Return"] = df.groupby("Ticker")["close"].pct_change()

print("\nData with Daily Return:")
print(df.head())


# STEP 6: TOP 10 GAINERS

returns = df.groupby("Ticker", group_keys=False).apply(
    lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
)
returns_df = returns.reset_index()
returns_df.columns = ["Ticker", "Yearly Return"]

top_10 = returns_df.sort_values(by="Yearly Return", ascending=False).head(10)

print("\nTop 10 Gainers:")
print(top_10)

# -------------------------------
# STEP 7: TOP 10 LOSERS
# -------------------------------
bottom_10 = returns_df.sort_values(by="Yearly Return", ascending=True).head(10)

print("\nTop 10 Losers:")
print(bottom_10)

# -------------------------------
# STEP 8: VOLATILITY
# -------------------------------
volatility = df.groupby("Ticker")["Daily Return"].std().reset_index()

volatility.columns = ["Ticker", "Volatility"]

top_volatile = volatility.sort_values(by="Volatility", ascending=False).head(10)

print("\nTop 10 Most Volatile Stocks:")
print(top_volatile)

# -------------------------------
# STEP 9: VISUALIZATION
# -------------------------------
top_volatile.plot(
    x="Ticker",
    y="Volatility",
    kind="bar",
    title="Top 10 Most Volatile Stocks"
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
# TASK 2: CUMULATIVE RETURN
# -------------------------------

# Step 1: Take top 5 stocks from top gainers
top5_stocks = top_10["Ticker"].head(5).tolist()

print("\nTop 5 Stocks:")
print(top5_stocks)


# Step 2: Filter data for these stocks
top5_df = df[df["Ticker"].isin(top5_stocks)].copy()


# Step 3: Sort data properly
top5_df = top5_df.sort_values(["Ticker", "date"])


# Step 4: Calculate cumulative return
top5_df["Cumulative Return"] = top5_df.groupby("Ticker")["Daily Return"].cumsum()
print("top_5")
print(top5_df)

# -------------------------------
# STEP 6: VISUALIZATION (LINE CHART)
# -------------------------------
plt.figure(figsize=(24,6))

for ticker in top5_stocks:
    stock_data = top5_df[top5_df["Ticker"] == ticker]
    plt.plot(stock_data["date"], stock_data["Cumulative Return"], label=ticker)

plt.legend()
plt.title("Top 5 Stocks - Cumulative Return")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.tight_layout()

plt.show()

#Task 3
sector_df = pd.read_csv("sector_data.csv")
#merging
df = df.merge(sector_df, on="Ticker", how="left")
#Sector wise performance
sector_performance = returns_df.merge(sector_df, on="Ticker", how="left")

sector_avg = sector_performance.groupby("Sector")["Yearly Return"].mean().reset_index()

print("\nSector-wise Performance:")
print(sector_avg)
#visualization
sector_avg.plot(
    x="Sector",
    y="Yearly Return",
    kind="bar",
    title="Average Yearly Return by Sector"
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Task 4
# Create pivot table

pivot_df = df.pivot(index="date", columns="Ticker", values="close")

print("\nPivot Table:")
print(pivot_df.head())

#Filter top stocks
top_stocks = top_10["Ticker"].tolist()
pivot_df = pivot_df[top_stocks]

#Correlation
correlation = pivot_df.corr()

print("\nCorrelation Matrix:")
print(correlation)

#Heatmap

import seaborn as sns

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation,
    cmap="coolwarm",
    annot=False
)

plt.title("Stock Price Correlation Heatmap")
plt.show()

#Task 5

monthly_returns = df.groupby(["month", "Ticker"]).apply(
    lambda x: (x["close"].iloc[-1] - x["close"].iloc[0]) / x["close"].iloc[0]
).reset_index()

monthly_returns.columns = ["Month", "Ticker", "Monthly Return"]

print("\nMonthly Returns:")
print(monthly_returns.head())

#Top 5 Gainers & Losers (per month)
print("\nTop 5 Gainers & Losers by Month:\n")

for month in monthly_returns["Month"].unique():

    month_data = monthly_returns[monthly_returns["Month"] == month]

    top5 = month_data.sort_values(by="Monthly Return", ascending=False).head(5)
    bottom5 = month_data.sort_values(by="Monthly Return", ascending=True).head(5)

    print(f"\nMonth: {month}")
    print("\nTop 5 Gainers:")
    print(top5[["Ticker", "Monthly Return"]])

    print("\nTop 5 Losers:")
    print(bottom5[["Ticker", "Monthly Return"]])

#Visualization
for month in monthly_returns["Month"].unique():

    month_data = monthly_returns[monthly_returns["Month"] == month]

    top5 = month_data.sort_values(by="Monthly Return", ascending=False).head(5)
    bottom5 = month_data.sort_values(by="Monthly Return", ascending=True).head(5)

    combined = pd.concat([top5, bottom5])

    combined.plot(
        x="Ticker",
        y="Monthly Return",
        kind="bar",
        title=f"Top 5 Gainers & Losers - {month}"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()