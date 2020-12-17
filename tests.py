import unittest
import unittest
import requests
from io import StringIO
from unittest.mock import patch, Mock, mock_open
from app import TrainLineAPP
from parse_csv import StationIDS
import csv
import json
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
API_ID = os.getenv('API_ID_')
KEY = os.getenv('KEY2')
app = TrainLineAPP()
S = StationIDS()
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

class TestParseLine(unittest.TestCase):
    def test_parse_line(self):
        line = ['station','','','station 2']
        expected_result = ['station', 'station 2']
        cleaned_line = S.parse_line(line)
        self.assertEqual(cleaned_line, expected_result)
        self.assertNotIn('', cleaned_line)
    
    def test_make_pairs(self):
        stations = [['birmingham', 'BIR', 'selly oak', 'SEL', 'Moor St', 'MOR']]
        expected_result = [['birmingham', 'BIR'], ['selly oak', 'SEL'], ['Moor St', 'MOR']]
        mapped_stations = S.make_pairs_names_ids(stations)
        self.assertEqual(mapped_stations, expected_result)
    
    @patch('csv.reader', return_value=['NEXT', ['Cwmbran', 'CWM', 'Meols Cop', 'MEC', '', '']])
    def test_get_stations(self, mock_csv):
        with patch('builtins.open') as mock_open:
            expected_result = [['Cwmbran', 'CWM', 'Meols Cop', 'MEC']]
            station_ids = S.get_stations('test.csv')
            self.assertEqual(station_ids, expected_result)
    @patch('app.TrainLineAPP.get_response', return_value={'departures': {'all': 'data'}})
    def test_get_station_data(self, mock_response):
        data = [{'Station Name': 'Abbey Wood', 'Station ID': 'ABW'}, {'Station Name': 'Gainsborough Central', 'Station ID': 'GNB'}]
        df = pd.DataFrame(data=data, dtype='string').set_index('Station Name')
        station = 'Abbey Wood'
        expected_result = 'data'
        expected_url = f'https://transportapi.com/v3/uk/train/station/ABW///timetable.json?app_id={API_ID}&app_key={KEY}&train_status=passenger'
        data = app.get_station_data(station, df)
        mock_response.assert_called()
        mock_response.assert_called_with(expected_url)
        self.assertEqual(data, expected_result)
        
    station = 'test'
    @patch('builtins.input', return_value=station)
    def test_display_destinations(self, mock_input):
        station = 'test'
        data = [{'destination_name': 'birmingham', 'other_thing': 'not_needed'}, 
        {'destination_name': 'leeds', 'other_thing': 'also_not_needed'},
        {'destination_name': 'birmingham', 'other_thing': 'not_needed'}]
        expected_list = set(['birmingham', 'leeds'])
        expected_result = (station, expected_list)
        self.assertEqual(app.display_destinations(data), expected_result)


    




if __name__ == '__main__':
    unittest.main()