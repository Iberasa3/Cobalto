import yfinance as yf
import pandas as pd
import sqlite3
import os

TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
DB_NAME = "cobalto_nasdaq_ml.db"


def initialize_db(conn):
    """Drops and creates the table to prevent duplicates on multiple runs."""
    cursor = conn.cursor()

    # Dropping the table if it exists for this test (in production we would use UPSERT)
    cursor.execute("DROP TABLE IF EXISTS raw_prices")
    conn.commit()


def extract_and_save(tickers, db_name):
    # Connect to SQLite (this will create the nasdaq_ml.db file in your folder)
    conn = sqlite3.connect(db_name)
    initialize_db(conn)

    for ticker in tickers:

        print(f"Downloading data for {ticker}...")
        # Downloading 2 years of daily data
        df = yf.download(ticker, period="2y", interval="1d")

        if df.empty:
            print(f" No data found for {ticker}")
            continue

        # Basic cleaning for SQL
        df = df.reset_index()  # Converts the date (used as index by yfinance) into a column
        df['Ticker'] = ticker  # Add the company name to filter later

        # Save to the database
        # Pandas handles the column creation automatically
        df.to_sql("raw_prices", conn, if_exists="append", index=False)
        print(f"{ticker} saved to the database.")

    conn.close()
    print(f"\nProcess completed. Database created at: {os.path.abspath(db_name)}")


# ---------------------------------------------------------------------------------------------------------------------

