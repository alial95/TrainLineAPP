import requests
from dotenv import load_dotenv
import os
from parse_csv import StationIDS
from geocode_distance import distance_between_km
from menu import Menu
import pandas as pd
load_dotenv()
API_ID = os.getenv('API_ID_')
KEY = os.getenv('KEY2')
AZURE_KEY = os.getenv('AZURE_MAPS')
S = StationIDS()
class TrainLineAPP:
    def __init__(self):
        self.station_ids = S.main()
        self.menu = Menu()


    def get_response(self, url):
        response = requests.get(url)
        assert response.status_code == 200
        return response.json()

    def get_response_location(self):    
        query = input('Please enter your address: ')
        url = f'https://atlas.microsoft.com/search/address/json?&subscription-key={AZURE_KEY}&api-version=1.0&language=en-US&query={query}'
        return self.get_response(url)

    def get_transportation_details(self, lat, lon):
        transport_types = ['train_station', 'bus_stop']
        for typ in transport_types:
            print(typ)
        transport_type = input('What transport type would you like to use? ')
        url = f'https://transportapi.com/v3/uk/places.json?app_id=8becbe0f&app_key=6f9f9f94705f5f992f9dfe0dbd391a96&lat={lat}&lon={lon}&type={transport_type}'
        return self.get_response(url)
    def build_url(self, code):
        url = f'https://transportapi.com/v3/uk/train/station/{code}///timetable.json?app_id={API_ID}&app_key={KEY}&train_status=passenger'
        return url

    def create_df(self, stations):
        df = pd.DataFrame(data=stations, dtype='string').set_index('Station Name')
        return df
    def get_station_data(self, station, df):
        code = df.loc[station]['Station ID']
        url = self.build_url(code)
        data = self.get_response(url)
        return data['departures']['all']
    def get_service_timetable(self, data):
        destination, destinations = self.display_destinations(data)
        for journey in data:
            if destination == journey['destination_name']:
                timetable = self.get_response(journey['service_timetable']['id'])
                return timetable
            else:
                print('You cant get to there from this station.')


    def show_service_timetable(self, data):
        for service in data['stops']:
            print(f'Station: {service["station_name"]} Departure Time: {service["aimed_departure_time"]} Arrival Time: {service["aimed_arrival_time"]}')
        


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
        destination, destinations = self.display_destinations(data)
        if destination in destinations:
            for train in data:
                if train['destination_name'] == destination:
                    print(f'The next train to {destination} is the {train["aimed_departure_time"]} service on platform {train["platform"]}')
                    break
        else:
            print('You cant get to this station from here.')
        
    def display_destinations(self, data):
        destinations = set([x['destination_name'] for x in data])
        for destination in destinations:
            print('Possible location: ', destination)
        destination = input('Where would you like to go? ')
        return destination, destinations
        
        
        
    
    def get_station_by_location(self):
        stations = self.station_ids
        df = self.create_df(stations)
        address = self.get_response_location()
        results = [x['address']['freeformAddress'] for x in address['results']]
        def display_results(query):
            # show the results of the query to the user 
            counter = 1
            for result in query:
                print(f'{result}: {counter}')
                counter += 1
            print('Here are the results from your query. Which location is the one youre after?')

        display_results(results)
        address_code = int(input('Enter the id number for your address: '))
        def filter_location(data, station):
            filtered = list(filter(lambda x: x['name'] == station, data['member']))
            return filtered[0]['latitude'], filtered[0]['longitude']
     
        user_lat = address['results'][address_code - 1]['position']['lat']
        user_longitude = address['results'][address_code - 1]['position']['lon']
        transport_details = self.get_transportation_details(user_lat, user_longitude)
        print([x['name'] for x in transport_details['member']])
        station = input('which station would you like to travel from? ')
        station_latitude, station_longitude = filter_location(transport_details, station)
        distance_to_station = distance_between_km(user_lat, user_longitude, station_latitude, station_longitude)
        print(f'The distance to the {station} train station is {distance_to_station}km')
        data = self.get_station_data(station, df)
        timetable_data = self.get_service_timetable(data)
        self.show_service_timetable(timetable_data)
        
    
            

    


    def run(self):
        while True:
            selection = self.menu._show_menu_and_get_selection()
            if selection == 1:
                self.get_station_by_location()
                input('Please hit enter to return to the main menu: ')
            elif selection == 2:
                self.show_stations(self.station_ids)
                input('Please hit enter to return to the main menu: ')
            elif selection == 3:
                self.get_station_request(self.station_ids)
                input('Please hit enter to return to the main menu: ')
            elif selection == 4:
                print('Bye!')
                exit()


if __name__ == '__main__':
    A = TrainLineAPP()
    A.run()