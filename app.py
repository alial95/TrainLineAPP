import requests
from dotenv import load_dotenv
import os
from parse_csv import StationIDS
import pandas as pd
load_dotenv()
API_ID = os.getenv('API_ID_')
KEY = os.getenv('KEY2')
S = StationIDS()
class TrainLineAPP:
    def __init__(self):
        self.station_ids = S.main()


    def get_response(self, url):
        response = requests.get(url)
        assert response.status_code == 200
        return response.json()
    def build_url(self, code):
        url = f'https://transportapi.com/v3/uk/train/station/{code}///timetable.json?app_id={API_ID}&app_key={KEY}&train_status=passenger'
        return url

    def create_df(self, stations):
        df = pd.DataFrame(data=stations, dtype='string')
        df = df.set_index('Station Name')
        return df
    def get_station_data(self, station, df):
        code = df.loc[station]['Station ID']
        url = self.build_url(code)
        data = self.get_response(url)
        return data['departures']['all']
    def get_station(self, stations):
            stations = [x['Station Name'] for x in stations]
            while True:
                try:
                    station = input('Please enter the name of the station: ')
                    if station not in stations:
                        print('Please enter a valid station name')
                    else:
                        return station
                except Exception as e:
                    return e
    def show_stations(self, stations):
        for station in stations[:10]:                  
            for key, value in station.items():
                print(f'Name: {value}')
        station = self.get_station(stations)
        
        df = self.create_df(stations)
        data = self.get_station_data(station, df)
        for i in data:
            if i['platform'] == '2':
                print(f'The next train on platform 2 is the {i["aimed_arrival_time"]} service to {i["destination_name"]}.')      #very basic functionality
                break
        
    
    def get_station_request(self, stations):
        station = self.get_station(stations)
        df = self.create_df(stations)
        data = self.get_station_data(station, df)
        destination = input('Where would you like to go? ')
        destinations = [x['destination_name'] for x in data]
        if destination in destinations:
            for train in data:
                if train['destination_name'] == destination:
                    print(f'The next train to {destination} is the {train["aimed_departure_time"]} service on platform {train["platform"]}')
                    break
        else:
            print('You cant get to this station from here.')

            

    


    def run(self):
        self.show_stations(self.station_ids)
        self.get_station_request(self.station_ids)


if __name__ == '__main__':
    A = TrainLineAPP()
    A.run()