import csv
from itertools import chain
import pandas as pd

class StationIDS:
    def __init__(self):
        pass


    def mapper(self, a):
        return {'Station Name': a[0], 'Station ID': a[1]}
    
    def mapper_2(self, a, b):
        return [a, b]
    


    def parse_line(self, line):
        lines = []
        for x in line:
            if x == '':
                continue
            else:
                lines.append(x)
        return lines
    def make_pairs(self, lst):
        
        if len(lst) == 2:
            return [lst[0], lst[1]]
        elif len(lst) == 4:
            return [lst[0], lst[1]], [lst[2], lst[3]]
        elif len(lst) == 6:
            return [lst[0], lst[1]], [lst[2], lst[3]], [lst[4], lst[5]]
        elif len(lst) == 8:
            return [lst[0], lst[1], [lst[2], lst[3]], [lst[4]], lst[5]], [lst[6], lst[7]]
    def make_pairs_names_ids(self, lst):
        codes = []
        names = []
        for row in lst:
            for name in row:
                if name == name.upper():
                    codes.append(name)
                else:
                    names.append(name)
        stations = list(map(self.mapper_2, (names), (codes)))
        return stations

    def get_stations(self):
        station_ids = []
        with open('station_codes.csv') as p:
            reader = csv.reader(p)
            next(reader)
            for line in reader:
                cleaned_line = self.parse_line(line)
                if len(cleaned_line) == 0:
                    continue
                else:
                    station_ids.append(cleaned_line)
       
        return station_ids
        
    def map_ids_names(self, station_ids):
        return list(map(self.mapper, (station_ids)))



    def main(self):
        stations = self.get_stations()
        clean_stations = self.make_pairs_names_ids(stations)
        mapped_stations = self.map_ids_names(clean_stations)
        return mapped_stations



