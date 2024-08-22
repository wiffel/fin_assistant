import requests
import requests_cache
from langchain_core.tools import tool
from typing import Optional
import os
from datetime import datetime
import pandas as pd
import io
from io import StringIO
from finasistant_app.config.settings import settings

# Install a persistent cache that never expires
requests_cache.install_cache("alphavantage_cache", expire_after=None)


BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")


if not API_KEY:
    raise ValueError("ALPHAVANTAGE_API_KEY environment variable is not set")


# Ensure the fetched_data directory exists
os.makedirs("fetched_data", exist_ok=True)


def save_to_csv(df, filename):
    file_path = os.path.join(str(settings.project_root), f'fetched_data/{filename}')
    df.to_csv(file_path, index=False)
    return file_path, df


@tool
def time_series_intraday_csv(
    symbol: str,
    interval: str,
    adjusted: bool = True,
    extended_hours: bool = True,
    month: Optional[str] = None,
    outputsize: str = "compact",
) -> dict:
    """
    Returns intraday time series of the equity specified, covering extended trading hours where applicable.
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "adjusted": "true" if adjusted else "false",
        "extended_hours": "true" if extended_hours else "false",
        "outputsize": outputsize,
        "datatype": "csv",
    }
    if month:
        params["month"] = month

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))

        filename = f"{symbol.lower()}_intraday_{interval}_{datetime.now().strftime('%Y%m%d')}.csv"
        csv_file_path, _ = save_to_csv(df, filename)

        buffer = StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        dataset_description = (
            f"Intraday time series data for {symbol} with {interval} interval. "
            f"Adjusted: {adjusted}, Extended hours: {extended_hours}, "
            f"Outputsize: {outputsize}, Month: {month if month else 'Not specified'}\n\n"
            f"DataFrame Info:\n{df_info}"
        )

        return {
            "csv_file_path": csv_file_path,
            "dataset_description": dataset_description,
        }
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


@tool
def time_series_daily_csv(symbol: str, outputsize: str = "compact") -> dict:
    """
    Returns daily time series of the global equity specified, covering 20+ years of historical data.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": outputsize,
        "datatype": "csv",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))

        filename = f"{symbol.lower()}_daily_{datetime.now().strftime('%Y%m%d')}.csv"
        csv_file_path, _ = save_to_csv(df, filename)

        buffer = StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        dataset_description = f"Daily time series data for {symbol}. Outputsize: {outputsize}\n\nDataFrame Info:\n{df_info}"

        return {
            "csv_file_path": csv_file_path,
            "dataset_description": dataset_description,
        }
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


@tool
def time_series_weekly_csv(symbol: str) -> dict:
    """
    Returns weekly time series of the global equity specified, covering 20+ years of historical data.
    """
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": API_KEY,
        "datatype": "csv",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))

        filename = f"{symbol.lower()}_weekly_{datetime.now().strftime('%Y%m%d')}.csv"
        csv_file_path, _ = save_to_csv(df, filename)

        buffer = StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        dataset_description = (
            f"Weekly time series data for {symbol}\n\nDataFrame Info:\n{df_info}"
        )

        return {
            "csv_file_path": csv_file_path,
            "dataset_description": dataset_description,
        }
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


@tool
def time_series_monthly_csv(symbol: str) -> dict:
    """
    Returns monthly time series of the global equity specified, covering 20+ years of historical data.
    """
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol,
        "apikey": API_KEY,
        "datatype": "csv",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))

        filename = f"{symbol.lower()}_monthly_{datetime.now().strftime('%Y%m%d')}.csv"
        csv_file_path, _ = save_to_csv(df, filename)

        buffer = StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        dataset_description = (
            f"Monthly time series data for {symbol}\n\nDataFrame Info:\n{df_info}"
        )

        return {
            "csv_file_path": csv_file_path,
            "dataset_description": dataset_description,
        }
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


@tool
def global_quote_json(symbol: str) -> dict:
    """
    Returns the latest price and volume information for a ticker of your choice.
    """
    params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": API_KEY}

    response = requests.get(BASE_URL, params=params)
    return response.json()


@tool
def symbol_search_json(keywords: str) -> dict:
    """
    Returns the best-matching symbols and market information based on keywords of your choice.
    """
    params = {"function": "SYMBOL_SEARCH", "keywords": keywords, "apikey": API_KEY}

    response = requests.get(BASE_URL, params=params)
    return response.json()


@tool
def market_status_json() -> dict:
    """
    Returns the current market status (open vs. closed) of major trading venues for equities, forex, and cryptocurrencies.
    """
    params = {"function": "MARKET_STATUS", "apikey": API_KEY}

    response = requests.get(BASE_URL, params=params)
    return response.json()


@tool
def realtime_options_csv(symbol: str, contract: Optional[str] = None) -> dict:
    """
    Returns realtime US options data with full market coverage for a given equity symbol.
    """
    params = {
        "function": "REALTIME_OPTIONS",
        "symbol": symbol,
        "apikey": API_KEY,
        "datatype": "csv",
    }
    if contract:
        params["contract"] = contract

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))

        filename = f"{symbol.lower()}_realtime_options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_file_path, _ = save_to_csv(df, filename)

        buffer = StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        dataset_description = f"Realtime options data for {symbol}"
        if contract:
            dataset_description += f" (Contract: {contract})"
        dataset_description += f"\n\nDataFrame Info:\n{df_info}"

        return {
            "csv_file_path": csv_file_path,
            "dataset_description": dataset_description,
        }
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


@tool
def historical_options_csv(symbol: str, date: Optional[str] = None) -> dict:
    """
    Returns the full historical options chain for a specific symbol, optionally on a specific date.
    """
    params = {
        "function": "HISTORICAL_OPTIONS",
        "symbol": symbol,
        "apikey": API_KEY,
        "datatype": "csv",
    }
    if date:
        params["date"] = date

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    csv_data = response.text
    df = pd.read_csv(io.StringIO(csv_data))

    filename = f"{symbol.lower()}_historical_options_{date if date else 'all'}.csv"
    csv_file_path, _ = save_to_csv(df, filename)

    buffer = StringIO()
    df.info(buf=buffer)
    df_info = buffer.getvalue()

    dataset_description = f"Historical options data for {symbol}"
    if date:
        dataset_description += f" on {date}"
    dataset_description += f"\n\nDataFrame Info:\n{df_info}"

    return {
        "csv_file_path": csv_file_path,
        "dataset_description": dataset_description,
    }


# List of all tools
tools = [
    time_series_intraday_csv,
    time_series_daily_csv,
    time_series_weekly_csv,
    time_series_monthly_csv,
    global_quote_json,
    symbol_search_json,
    market_status_json,
    realtime_options_csv,
    historical_options_csv,
]
