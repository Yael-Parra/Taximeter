import pytest
import json
import os
import datetime
from unittest.mock import patch, mock_open
from intermediate_level.main_taximeter_intermediate_level import load_rates, demand_level, history_ride, logs_ride

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
def test_history_ride():
    total_ride = 1.0
    demand_multiplier = 1.1

    with patch("builtins.open", mock_open()) as mocked_file:
        history_ride(total_ride, demand_multiplier)
        mocked_file.assert_called_once_with("intermediate_level/history_ride.json", "a")
        handle = mocked_file()
        assert handle.write.call_count == 22

#---------------------------------------------------------------------------------------

LOGS_PATH = os.path.join("intermediate_level", "logs_ride.log")

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if os.path.exists(LOGS_PATH):
        os.remove(LOGS_PATH)

def test_logs_ride_success():
    message = "Test log entry"
    
    with patch("builtins.open", mock_open()) as mocked_file:
        logs_ride(message)
   
        mocked_file.assert_called_once_with(LOGS_PATH, "a")
        
        written_data = mocked_file().write.call_args[0][0]
        
        print("Written data:", written_data)
        
        assert written_data.strip()  
        
        assert message in written_data
        assert "INFO" in written_data

def test_logs_ride_file_error():
    message = "Test log entry"
    
    with patch("builtins.open", side_effect=IOError("File error")):
        with patch("logging.error") as mock_logging_error:
            logs_ride(message)
            mock_logging_error.assert_called_once_with("Error saving ride logs: File error")

# For running (be sure to be on the RIGHT FOLDER!!!) the test: pytest test_taximeter_intermediate.py