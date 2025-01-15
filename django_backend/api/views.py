from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .yf_fetch import *
from datetime import date

@api_view(["GET"])
def index(request):
    return render(request, "index.html")

@api_view(["GET"])
def get_balance_sheet(request, ticker):
    try:
        final_json_file = get_balance_sheet_as_json(ticker)
        return Response(final_json_file)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def get_cash_flow(request, ticker):
    try:
        final_json_file = get_cash_flow_as_json(ticker)
        return Response(final_json_file)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def get_historical_data(request, ticker):
    try:
        # Extract query parameters with defaults
        period = request.query_params.get("period", "1mo")  # Default to '1mo'
        interval = request.query_params.get("interval", "1d")  # Default to '1d'

        # Fetch historical data using the utility function
        historical_data = get_historical_data_with_kwargs(
            tickers=ticker,
            period=period,
            interval=interval
        )

        # Convert JSON string to Python object for Response
        historical_data_json = json.loads(historical_data)

        return Response(historical_data_json)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def get_sector_and_industry(request, ticker):
    try:
        data = yf.Ticker(ticker).info
        sector = data.get("sector", "N/A")
        industry = data.get("industry", "N/A")
        sector_and_industry_data = {"ticker": ticker, "sector": sector, "industry": industry}
        return Response(sector_and_industry_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

@api_view(["GET"])
def get_calendar(request, ticker):
    try:
        my_data = yf.Ticker(ticker)
        calendar_data = my_data.calendar
        
        if calendar_data is None:
            return Response({"error": "No calendar data available"})
            
        # Use the custom encoder to handle date objects
        return Response(json.loads(json.dumps(calendar_data, cls=DateEncoder)))
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)
