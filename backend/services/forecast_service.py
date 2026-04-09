"""
Forecast Service
================
Loads CNN+LSTM forecast data from bihar_predictions.csv and provides
it to the API routes.
"""

import os
import pandas as pd
import numpy as np

# Paths relative to repository root (matches dispatch_service/battery_service)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FORECAST_CSV = os.path.join(ROOT_DIR, "CNN+LSTM-FORECASTER", "data", "bihar_predictions.csv")

_forecast_cache = None


def _load_forecast():
    """Load and cache forecast data."""
    global _forecast_cache
    if _forecast_cache is not None:
        return _forecast_cache

    if not os.path.exists(FORECAST_CSV):
        return pd.DataFrame()

    df = pd.read_csv(FORECAST_CSV, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Clamp negatives (physics)
    for col in ["solar_power_q10", "solar_power_q50", "solar_power_q90",
                "wind_power_q10", "wind_power_q50", "wind_power_q90"]:
        if col in df.columns:
            df[col] = df[col].clip(lower=0)

    _forecast_cache = df
    return df


def get_forecast_data(limit=None):
    """Return forecast data as list of dicts for JSON serialization."""
    df = _load_forecast()
    if df.empty:
        return []
    if limit:
        df = df.tail(limit)

    # Convert timestamp to ISO string for JSON
    result = df.copy()
    result["timestamp"] = result["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    return result.to_dict(orient="records")


def get_latest_forecast():
    """Return the most recent forecast snapshot."""
    df = _load_forecast()
    if df.empty:
        return {}
    last = df.iloc[-1]
    return {
        "timestamp": last["timestamp"].isoformat(),
        "solar": {
            "q10": round(float(last.get("solar_power_q10", 0)), 2),
            "q50": round(float(last.get("solar_power_q50", 0)), 2),
            "q90": round(float(last.get("solar_power_q90", 0)), 2),
        },
        "wind": {
            "q10": round(float(last.get("wind_power_q10", 0)), 2),
            "q50": round(float(last.get("wind_power_q50", 0)), 2),
            "q90": round(float(last.get("wind_power_q90", 0)), 2),
        },
        "load": {
            "q10": round(float(last.get("load_demand_q10", 0)), 2),
            "q50": round(float(last.get("load_demand_q50", 0)), 2),
            "q90": round(float(last.get("load_demand_q90", 0)), 2),
        },
    }


def get_forecast_summary():
    """Return summary statistics for the forecast dataset."""
    df = _load_forecast()
    if df.empty:
        return {}
    return {
        "total_records": len(df),
        "date_range": {
            "start": df["timestamp"].min().isoformat(),
            "end": df["timestamp"].max().isoformat(),
        },
        "solar_avg_kw": round(float(df["solar_power_q50"].mean()), 2),
        "wind_avg_kw": round(float(df["wind_power_q50"].mean()), 2),
        "load_avg_kw": round(float(df["load_demand_q50"].mean()), 2),
        "solar_max_kw": round(float(df["solar_power_q50"].max()), 2),
        "wind_max_kw": round(float(df["wind_power_q50"].max()), 2),
        "load_max_kw": round(float(df["load_demand_q50"].max()), 2),
    }
