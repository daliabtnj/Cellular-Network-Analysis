import json
import sys
import random
import math
from collections import defaultdict

# function to display the menu
def display_menu():
    print("\nPlease select option from the menu:")
    print("\t1. Display Global Statistics")
    print("\t2. Display Base Station Statistics")
    print("\t\t2.1. Statistics for a random station")
    print("\t\t2.2. Choose a station by Id")
    print("\t3. Check Coverage")
    print("\t4. Exit")

# create classes for points, antennas and base stations
class Points:
    def __init__(self, lat, lon, power):
        self.lat = lat
        self.lon = lon
        self.power = power

class Ants:
    def __init__ (self, ant_id, frq, bw, points):
        self.id = ant_id
        self.frq = frq
        self.bw = bw
        self.points = [Points(*pt) for pt in points]

class BaseStation:
    def __init__(self, base_id, lat, lon, antennas):
        self.id = base_id
        self.lat = lat
        self.lon = lon
        self.antennas = [Ants(ant["id"], ant["frq"], ant["bw"], ant["pts"]) for ant in antennas]


def calculate_global_statistics(base_stations, grid_point, tolerance = 1e-6):

    # total nb of stations
    total_base_stations = len(base_stations) 

    # create list that contains the nb of antennas for each stations
    antennas_per_bs = [len(bs.antennas) for bs in base_stations] 

    # calculates total nb of antennas
    total_antennas = sum(antennas_per_bs) 
    max_antenna_bs = max(antennas_per_bs) 
    min_antenna_bs = min(antennas_per_bs)
    avg_antennas_bs = sum(antennas_per_bs) / total_base_stations


    # create a list with all points covered by antennas
    points_coverage = defaultdict(int)
    antenna_coverage_count = defaultdict(int)
    # automatically create key and initialize its value to 0 if key isn't in dictionary

    # go trhough every point in grid, check if they match with points from json file to find covered points
    # create dictionary that has as value which is the number of antennas it is covered by
    for point in grid_point:
        for bs in base_stations:
            for ant in bs.antennas:
                for pt in ant.points:
                    if math.isclose(point[0], pt.lat, abs_tol=tolerance) and math.isclose(point[1], pt.lon, abs_tol=tolerance):
                        points_coverage[point] += 1
                        antenna_coverage_count[(bs.id, ant.id)] += 1

    # nb of points covered by one, more than one, and no antenna
    one_antenna = sum(1 for value in points_coverage.values() if value == 1)
    more_antenna = sum(1 for value in points_coverage.values() if value >1)
    no_antenna = len(grid_point) - len(points_coverage)

    # max nb of antennas that cover one point
    max_antenna_one = max(points_coverage.values(), default = 0)

    # average nb of antennas covering a square
    average_covered = (sum(points_coverage.values())) / len(points_coverage)

    # percentage area covered by provider
    percentage_area = 100 * len(points_coverage) / len(grid_point) 

    # find the antenna and base station covering the maximum number of points
    max_covered_antenna = max(antenna_coverage_count, key=antenna_coverage_count.get, default=(None, None))


    # Print statistics
    print("\nGLOBAL STATISTICS:")
    print(f"Total number of base stations: {total_base_stations}")
    print(f"Total number of antennas: {total_antennas}")
    print(f"Max, min, average antennas in a base station: {max_antenna_bs}, {min_antenna_bs}, {avg_antennas_bs:.2f}")
    print(f"Points covered by exactly one antenna: {one_antenna}")
    print(f"Points covered by more than one antenna: {more_antenna}")
    print(f"Points covered by no antennas: {no_antenna}")
    print(f"Max antennas covering a single point: {max_antenna_one}")
    print(f"Average antennas covering each point: {average_covered:.2f}")
    print(f"Percentage of area covered: {percentage_area:.2f}%")
    if max_covered_antenna != (None, None):
        print(f"Base station and antenna covering the maximum number of points: base station {max_covered_antenna[0]}, antenna {max_covered_antenna[1]}")
    else:
        print("No points are covered by any antennas.")

def calculate_base_station_statistics(base_station, grid_points, tolerence = 1e-6):
    antennas_nb = len(base_station.antennas)
    points_coverage = defaultdict(int)
    antenna_coverage_count = defaultdict(int)    

    for point in grid_points:
        for ant in base_station.antennas:
            for pt in ant.points:
                if math.isclose(point[0], pt.lat, abs_tol= tolerence) and math.isclose(point[1], pt.lon, abs_tol = tolerence):
                    points_coverage[point] +=1
                    antenna_coverage_count[ant.id] +=1
    
    one_antenna = sum(1 for value in points_coverage.values() if value == 1 )
    more_antenna = sum(1 for value in points_coverage.values() if value > 1)
    no_antenna = len(grid_points) - len(points_coverage)

    max_covered = max(points_coverage.values(), default = 0)
    average_covered = sum(points_coverage.values()) / len(points_coverage)
    percentage_area = len(points_coverage) * 100 / len(grid_points)

    max_antenna = max(antenna_coverage_count, key = antenna_coverage_count.get, default = None)

    print(f"\nBASE STATION #{base_station.id} STATISTICS:")
    print(f"Total number of antennas: {antennas_nb}")
    print(f"Points covered by exactly one antenna: {one_antenna}")
    print(f"Points covered by more than one antenna: {more_antenna}")
    print(f"Points covered by no antennas: {no_antenna}")
    print(f"Max antennas covering a single point: {max_covered}")
    print(f"Average antennas covering each point: {average_covered:.2f}")
    print(f"Percentage of area covered: {percentage_area:.2f}%")
    if max_antenna is not None:
        print(f"Antenna covering the maximum number of points: antenna {max_antenna}")
    else:
        print("No points are covered by any antennas.")

def find_nearest_antenna(lat, lon, base_stations):
    min_distance = float('inf')
    nearest_antenna_info = None

    for bs in base_stations:
        for ant in bs.antennas:
            for pt in ant.points:
                distance = math.sqrt((lat - pt.lat) ** 2 + (lon - pt.lon) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_antenna_info = (bs.id, ant.id, pt.lat, pt.lon, pt.power)

    return nearest_antenna_info

def check_coverage(lat, lon, base_stations, tolerance=1e-6):
    covered_by = []
    
    for bs in base_stations:
        for ant in bs.antennas:
            for pt in ant.points:
                if math.isclose(lat, pt.lat, abs_tol=tolerance) and math.isclose(lon, pt.lon, abs_tol=tolerance):
                    covered_by.append((bs.id, ant.id, pt.power))
    
    if covered_by:
        print(f"\nThe point ({lat}, {lon}) is covered by the following antennas:")
        for bs_id, ant_id, power in covered_by:
            print(f"Base station {bs_id}, Antenna {ant_id}, Power: {power}")
    else:
        nearest_antenna = find_nearest_antenna(lat, lon, base_stations)
        if nearest_antenna:
            bs_id, ant_id, ant_lat, ant_lon, ant_power = nearest_antenna
            print(f"\nThe point ({lat}, {lon}) is not explicitly covered by any antenna.")
            print(f"The nearest antenna is at ({ant_lat}, {ant_lon}) with base station {bs_id} and antenna {ant_id}. Power: {ant_power}")
        else:
            print("\nNo antennas found in the data.")

def main():
    if len(sys.argv) != 2:
        print("Please enter arguments correctly : python3 <your_code.py> <test_file_json.json>")
        return
    
    print("\nWelcome to Dalia's cellular network analysis program !")
    print("********************************************************")
    
    # process the file
    input_file = sys.argv[1]

    # try to open the file, error if it doesn't open
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
        print("\nData was loaded successfully from file...\n")

        # process data
        min_lat = data["min_lat"]
        max_lat = data["max_lat"]
        min_lon = data["min_lon"]
        max_lon = data["max_lon"]
        step = data["step"]

        # create a list with coordinates of all points in the grid
        grid_points = []
    
        lat = min_lat
    
        while lat <= max_lat + 1e-6:
            lon = min_lon
            while lon <= max_lon + 1e-6:
                grid_points.append((lat, lon))
                lon += step
            lat += step

        # create base station obj
        base_stations = [BaseStation(bs["id"], bs["lat"], bs["lon"], bs["ants"]) for bs in data["baseStations"]]

        while True:
            display_menu()
            choice = input("\nEnter your choice: ")

            if choice == "1":
                calculate_global_statistics(base_stations, grid_points)
            elif choice == "2":
                print("\nPlease choose between 2.1 and 2.2 ")
            elif choice == "2.1":
                calculate_base_station_statistics(random.choice(base_stations), grid_points)
            elif choice == "2.2":
                while True:
                    station_id = int(input("Please enter station id: "))
                    station = next((bs for bs in base_stations if bs.id == station_id), None)
                    if station:
                        calculate_base_station_statistics(station, grid_points)
                        break
                    else:
                        print("Invalid base station ID. Please try again.")
            elif choice == "3":
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
                check_coverage(lat, lon, base_stations)
            elif choice == "4":
                print("\nhope you had fun, exiting the program ... ")
                break
            else:
                print("Hmmm ... you seem to have selected an invalid choice :0 ")
                print("I'll grant you another try, please try again by entering a valid choice! ")

                

        print(f"\nThanks for using my program, have a great day :) !!")
        print(f"***               - Dalia <3 -                  ***")
    except FileNotFoundError:
        print("Sorry, couldn't find the file :(")
    except json.JSONDecodeError:
        print("Error: the file is not a valid JSON file")
    

main()