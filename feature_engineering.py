# feature_engineering.py
import sqlite3
import pandas as pd


def load_raw_data(db_name):
    """Reads raw prices from the SQLite database."""
    conn = sqlite3.connect(db_name)
    # Ordering by Ticker and Date is crucial for time series calculations
    query = "SELECT * FROM raw_prices ORDER BY Ticker, Date"
    df = pd.read_sql(query, conn, parse_dates=['Date'])
    conn.close()
    return df


def create_features(df):
    """Calculates technical indicators and sets up the target variable."""
    processed_dfs = []

    # Group by Ticker to avoid mixing Apple's prices with Microsoft's
    for ticker, group in df.groupby('Ticker'):
        group = group.sort_values('Date').copy()

        # --- FEATURE ENGINEERING ---

        # 1. Daily Return (Percentage change)
        group['Daily_Return'] = group['Close'].pct_change()

        # 2. Volatility (10-day rolling standard deviation of returns)
        group['Volatility_10d'] = group['Daily_Return'].rolling(window=10).std()

        # 3. Simple Moving Averages (SMA)
        group['SMA_20'] = group['Close'].rolling(window=20).mean()
        group['SMA_50'] = group['Close'].rolling(window=50).mean()

        # --- TARGET VARIABLE (What the ML model will predict) ---

        # Next day's close price
        group['Next_Day_Close'] = group['Close'].shift(-1)
        # Target: 1 if tomorrow's price is higher than today's, 0 otherwise
        group['Target'] = (group['Next_Day_Close'] > group['Close']).astype(int)

        # Drop rows with NaN values (created by rolling windows and shifting)
        group = group.dropna()

        # CRITICAL: Drop 'Next_Day_Close' to prevent data leakage
        group = group.drop(columns=['Next_Day_Close'])

        processed_dfs.append(group)

    final_df = pd.concat(processed_dfs, ignore_index=True)
    return final_df


def save_features(df, db_name):
    """Saves the engineered features to a new table in SQLite."""
    conn = sqlite3.connect(db_name)
    df.to_sql("ml_features", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Feature engineering complete. Saved {len(df)} rows to 'ml_features' table.")


def run_feature_engineering(db_name):
    """Main function to execute the feature engineering pipeline."""
    print("Loading raw data...")
    raw_df = load_raw_data(db_name)

    print("Calculating financial features...")
    features_df = create_features(raw_df)

    print("Saving processed data...")
    save_features(features_df, db_name)