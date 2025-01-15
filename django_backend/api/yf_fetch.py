import yfinance as yf
import pandas as pd
import json
from datetime import datetime

# Helper Functions
def convert_timestamps_to_strings(data):
    if isinstance(data, dict):
        return {str(key): convert_timestamps_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_timestamps_to_strings(item) for item in data]
    else:
        return data

def convert_timestamp_to_string(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, (datetime, pd.Timestamp)) else str(timestamp)

def convert_data_to_json(data):
    if isinstance(data, pd.DataFrame):  # Handle DataFrames
        data_dict = data.to_dict()
    elif isinstance(data, dict):  # Already a dictionary
        data_dict = data
    else:  # Handle unsupported types
        return json.dumps({"error": "Unsupported data type"}, indent=4)

    # Convert timestamps to strings
    data_dict = convert_timestamps_to_strings(data_dict)
    return json.dumps(data_dict, indent=4)

def convert_to_json(data):
    if isinstance(data, dict):  # Handle dictionaries
        for key, value in data.items():
            if isinstance(value, (datetime, pd.Timestamp)):
                data[key] = convert_timestamp_to_string(value)
    elif isinstance(data, pd.DataFrame):  # Handle DataFrames
        data = data.reset_index()
        for col in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[col]):
                data[col] = data[col].apply(convert_timestamp_to_string)
        data = data.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
    elif isinstance(data, pd.Series):  # Handle Series
        data = data.to_dict()

    return json.dumps(data, indent=4)

# Function to fetch balance sheet as JSON for single ticker
def get_balance_sheet_as_json(ticker_symbol, **kwargs):
    try:
        my_data = yf.Ticker(ticker_symbol)
        my_balance_sheet = my_data.balance_sheet
        balance_sheet_json = convert_data_to_json(my_balance_sheet)
        return balance_sheet_json
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

# Function to fetch cash flow as JSON for single ticker
def get_cash_flow_as_json(ticker_symbol, **kwargs):
    try:
        my_data = yf.Ticker(ticker_symbol)
        my_cash_flow = my_data.cashflow
        cash_flow_json = convert_data_to_json(my_cash_flow)
        return cash_flow_json
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

# Function to fetch historical data for single ticker with parameters
def get_historical_data_with_kwargs(tickers, **kwargs):
    """Fetch historical data for single or multiple tickers with additional parameters."""
    if isinstance(tickers, str):
        tickers = [tickers]

    result = {}
    for ticker in tickers:
        data = yf.Ticker(ticker).history(**kwargs)
        result[ticker] = convert_to_json(data)
    return result if len(result) > 1 else result[tickers[0]]

# Function to fetch sector and industry data for single or multiple tickers
def get_sector_and_industry(tickers, **kwargs):
    if isinstance(tickers, str):
        tickers = [tickers]

    result = {}
    for ticker in tickers:
        info = yf.Ticker(ticker).info
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        result[ticker] = {"sector": sector, "industry": industry}
    return convert_to_json(result) if len(result) > 1 else convert_to_json(result[tickers[0]])

# Function to fetch calendar data for a single ticker
# def get_calendar_as_json(ticker_symbol):
#     try:
#         my_data = yf.Ticker(ticker_symbol)
#         my_calendar = my_data.calendar  # Typically a dictionary

#         if isinstance(my_calendar, dict):  # Directly convert if it's a dictionary
#             # Convert all datetime/date objects to strings in the calendar dictionary
#             my_calendar = convert_dates_to_strings(my_calendar)
#             calendar_json = json.dumps(my_calendar, indent=4)
#         else:
#             raise ValueError("Unexpected data format for calendar")

#         return calendar_json
#     except Exception as e:
#         return json.dumps({"error": str(e)}, indent=4)

# def get_calendar_as_json(ticker_symbol):
    try:
        my_data = yf.Ticker(ticker_symbol)
        my_calendar = my_data.calendar

        # Handle the case where calendar might be None
        if my_calendar is None:
            return json.dumps({"error": "No calendar data available"}, indent=4)

        # Ensure my_calendar is a dictionary before processing
        if not isinstance(my_calendar, dict):
            return json.dumps({"error": "Unexpected calendar data format"}, indent=4)

        # Convert all datetime/date objects to strings in the calendar dictionary
        converted_calendar = convert_dates_to_strings(my_calendar)
        return json.dumps(converted_calendar, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

# Updated convert_dates_to_strings function for better type checking
# def convert_dates_to_strings(data):
    if data is None:
        return None
    if isinstance(data, dict):
        return {key: convert_dates_to_strings(value) for key, value in data.items()}
    if isinstance(data, list):
        return [convert_dates_to_strings(item) for item in data]
    if isinstance(data, (datetime, pd.Timestamp)):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(data, datetime.date):
        return data.strftime("%Y-%m-%d")
    return data

# In your yf_fetch.py
def get_calendar_as_json(ticker_symbol):
    try:
        my_data = yf.Ticker(ticker_symbol)
        my_calendar = my_data.calendar

        # Handle the case where calendar might be None
        if my_calendar is None:
            return json.dumps({"error": "No calendar data available"}, indent=4)

        # Convert the calendar data to a dictionary if it isn't already
        if hasattr(my_calendar, 'to_dict'):
            my_calendar = my_calendar.to_dict()
        elif not isinstance(my_calendar, dict):
            return json.dumps({"error": "Unexpected calendar data format"}, indent=4)

        # Convert timestamps to strings
        converted_calendar = convert_timestamps_to_strings(my_calendar)
        return json.dumps(converted_calendar, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

def convert_timestamps_to_strings(data):
    if isinstance(data, dict):
        return {str(key): convert_timestamps_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_timestamps_to_strings(item) for item in data]
    elif isinstance(data, (datetime, pd.Timestamp)):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(data, pd.Series):
        return data.to_dict()
    elif isinstance(data, pd.DataFrame):
        return data.to_dict()
    else:
        return data

# Example usage
if __name__ == "__main__":

    single_ticker = "AAPL"
    multiple_tickers = ["AAPL", "MSFT", "GOOGL"]

    # # Balance sheet for a single ticker
    # print("Balance Sheet for Single Ticker:")
    # print(get_balance_sheet_as_json(single_ticker))

    # # Cash flow for a single ticker
    # print("\nCash Flow for Single Ticker:")
    # print(get_cash_flow_as_json(single_ticker))

    # # Historical data for single ticker
    # print("\nHistorical Data for Single Ticker:")
    # print(get_historical_data(single_ticker))

    # # Historical data for single ticker with parameters
    # print("\nHistorical Data for Single Ticker:")
    # print(get_historical_data_with_kwargs(single_ticker, interval="1h", period="1mo"))

    # # Sector / Industry information for single ticker
    # print("\nSector and Industry Data for Single Ticker:")
    # print(get_sector_and_industry(single_ticker))

    # # Sector / Industry information for multiple tickers
    # print("\nSector and Industry Data for Multiple Tickers:")
    # print(get_sector_and_industry(multiple_tickers))

    # # Calendar information for single ticker
    # print("\nCalendar Information for Single Ticker:")
    # print(get_calendar_as_json(single_ticker))
