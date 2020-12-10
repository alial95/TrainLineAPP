import unittest
import unittest
import requests
from unittest.mock import patch
from app import TrainLineAPP
import json
app = TrainLineAPP()
class TestResponse(unittest.TestCase):
    def test_response(self):
        with patch('requests.Response.json') as mock_request:
            url = 'http://bbc.co.uk'
            mock_request.return_value.json = {"Fake: content"}
            mock_request.return_value.status_code = 200
            response = app.get_response(url)
            self.assertEqual(response, mock_request.return_value)
            self.assertEqual(response.status_code, mock_request.return_value.status_code)

class TestGetStation(unittest.TestCase):
    station = 'test'
    
    @patch('builtins.input', return_value=station)
    def test_input(self, mock_input):
        stations = [{'Station Name': 'test'}, {'Station Name': 'Test'}]
        station_names = ['test', 'Test']
        station = 'test'
        bad_station = 'Euston'
        result = app.get_station(stations)
        self.assertEqual(result, station)
        self.assertNotEqual(result, bad_station)
        self.assertIn(result, station_names)

if __name__ == '__main__':
    unittest.main()