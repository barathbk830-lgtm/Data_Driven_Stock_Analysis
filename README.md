# Data_Driven_Stock_Analysis
Project Overview
This project analyzes stock market data using Python and visualizes insights using Streamlit.
It includes:
- Volatility Analysis
- Cumulative Return Analysis
- Sector-wise Performance
- Correlation Analysis
- Monthly Gainers & Losers
- ## Project Structure
Stock Analysis/
│
├── main.py # Data processing & analysis
├── app.py # Streamlit dashboard
├── all_stock_data.csv # Processed stock data
├── sector_data.csv # Sector mapping
├── output/ # Individual stock CSVs
├── README.md # Project documentation

##Technologies Used
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- YAML


##Features

### Volatility Analysis
- Measures stock risk using standard deviation of daily returns
- Displays top 10 most volatile stocks

### Cumulative Return
- Shows growth of top performing stocks over time
- Line chart visualization
  
### Sector-wise Performance
- Maps stocks to sectors using CSV
- Calculates average return per sector

### Correlation Analysis
- Shows relationship between stock prices
- Heatmap visualization

### Monthly Analysis
- Identifies top 5 gainers & losers for each month
- Helps track short-term trends

- ## Streamlit Dashboard

To run the dashboard:
streamlit run app.py

##Conclusion
This project provides insights into stock performance, risk, and trends using data-driven techniques.
 
