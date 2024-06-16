# Cellular Network Coverage Analysis Program

This Python program analyzes the coverage and statistics of a cellular network provider based on a provided JSON file. The file includes information about base stations, antennas, and the geographical points they cover. The program offers features to display global statistics, individual base station statistics, and check coverage for specific coordinates.

## Features
- **Global Statistics:**
  - Total number of base stations and antennas
  - Max, min, and average number of antennas per base station
  - Points covered by exactly one, more than one, and no antennas
  - Max and average number of antennas covering a single point
  - Percentage of area covered
  - ID of the base station and antenna covering the maximum number of points
- **Base Station Statistics:**
  - Total number of antennas in a base station
  - Points covered by exactly one, more than one, and no antennas
  - Max and average number of antennas covering a single point
  - Percentage of area covered by the base station
  - ID of the antenna covering the maximum number of points
- **Coverage Check:**
  - Check if a specific coordinate is covered by any antenna
  - List base stations and antennas covering the coordinate with power levels
  - If not covered, display the nearest antenna and its details

## Usage
Run the script with a JSON input file: `python3 cellular_network.py test_file.json`

## Example JSON File
The repository includes an example JSON file (`test_file.json`) for testing purposes.

