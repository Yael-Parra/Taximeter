import pytest
import json
import os
import datetime
from unittest.mock import patch, mock_open
from main_taximeter_intermediate_level import load_rates, demand_level, ride_history, ride_logs

#---------------------------------------------------------------------------------------
def test_load_rates():
    # Create a mock rates.json file to verify against it
    mock_rates = {
        "rates": {
            "base": {
                "stationary": 0.02,
                "motion": 0.05
            },
            "demand_multipliers": {
                "normal": 1.0,
                "low": 0.9,
                "high": 1.1
            }
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_rates))):
        rates = load_rates()
        assert rates["base"]["stationary"] == 0.02
        assert rates["base"]["motion"] == 0.05
        assert rates["demand_multipliers"]["normal"] == 1.0

#---------------------------------------------------------------------------------------
def test_demand_level(monkeypatch):

    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return cls(2025, 2, 15, 8, 0)  # yyyy.mm.dd hh:ss 
        def today(cls):
            return cls(2025, 2, 15, 8, 0)
        def fromtimestamp(cls, timestamp):
            return cls(2025, 2, 15, 8, 0)

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)

    demand = demand_level()
    assert "🟢 Low Demand: Discounted rate for off-peak hours will be applied" in demand

#---------------------------------------------------------------------------------------
def test_ride_history():
    total_ride = 1.0
    demand_multiplier = 1.1

    with patch("builtins.open", mock_open()) as mocked_file:
        ride_history(total_ride, demand_multiplier)
        mocked_file.assert_called_once_with("intermediate_level/ride_history.json", "a")
        handle = mocked_file()
        assert handle.write.call_count == 22

#---------------------------------------------------------------------------------------
def test_log_ride():
    message = "Total ride: 10.0, Demand multiplier: 1.1"

    with patch("builtins.open", mock_open()) as mocked_file:
        ride_logs(message)
        mocked_file.assert_called_once_with("intermediate_level/logs_ride.log", "a")
        
        handle = mocked_file()
        print(handle.write.call_args_list)
        assert handle.write.call_count == 1 

# For running (be sure to be on the RIGHT FOLDER!!!) the test: pytest test_taximeter_intermediate.py