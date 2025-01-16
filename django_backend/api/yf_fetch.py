import yfinance as yf
import pandas as pd
import json
from datetime import datetime, date

# Helper Functions

def convert_timestamp_to_string(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, (datetime, pd.Timestamp)) else str(timestamp)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Main Functions

def get_balance_sheet_as_json(ticker_symbol, **kwargs):
    bs = yf.Ticker(ticker_symbol).balance_sheet
    bs_json_cleaned = {
        str(key): {
            sub_key: (None if pd.isna(sub_value) or sub_value in [float('inf'), float('-inf')] else sub_value)
            for sub_key, sub_value in value.items()
        }
        for key, value in bs.to_dict().items()
    }
    return bs_json_cleaned

def get_cash_flow_as_json(ticker_symbol, **kwargs):
    cf = yf.Ticker(ticker_symbol).cashflow
    cf_json_cleaned = {
        str(key): {
            sub_key: (None if pd.isna(sub_value) or sub_value in [float('inf'), float('-inf')] else sub_value)
            for sub_key, sub_value in value.items()
        }
        for key, value in cf.to_dict().items()
    }
    return cf_json_cleaned

def get_historical_data_as_json(ticker_symbol, **kwargs):
    historical_data = yf.Ticker(ticker_symbol).history(**kwargs)
    # handle pandas dataframe
    if isinstance(historical_data, pd.DataFrame):
        historical_data = historical_data.reset_index()
        for col in historical_data.columns:
            if pd.api.types.is_datetime64_any_dtype(historical_data[col]):
                historical_data[col] = historical_data[col].apply(convert_timestamp_to_string)
        # Convert DataFrame to list of dictionaries
        historical_data = historical_data.to_dict(orient="records")
    return json.loads(json.dumps(historical_data))

def get_sector_and_industry_as_json(ticker_symbol, **kwargs):
    info = yf.Ticker(ticker_symbol).info
    result = {
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A")
    }
    return result

def get_cal_as_json(ticker_symbol, **kwargs):
    cal = yf.Ticker(ticker_symbol).calendar
    if cal is None:
        return json.dumps({"error": "No calendar data available"})
    return json.loads(json.dumps(cal, cls=DateEncoder))

# Example usage
if __name__ == "__main__":

    single_ticker = "AAPL"

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
    # print(get_historical_data_as_json(single_ticker, interval="1h", period="1mo"))

    # # Sector / Industry information for single ticker
    # print("\nSector and Industry Data for Single Ticker:")
    # print(get_sector_and_industry_as_json(single_ticker))

    # # Calendar information for single ticker
    # print("\nCalendar Information for Single Ticker:")
    # print(get_calendar_as_json(single_ticker))
