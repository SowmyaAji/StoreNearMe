#!/usr/bin/env pipenv run python
import csv
import sys
import geocoder
import argparse
import math
import json

def store_locations(read_file="store-locations.csv"):
    """read the CSV file and return all its contents as a list for use in otehr functions below"""
    with open(read_file) as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def nearest(latitude, longitude, store_locations):
    """Find the nearest store using latitute, longitude and the store_locations given in the file"""
    nearest = None
    distance = sys.maxsize
    latitude = float(latitude)
    longitude = float(longitude)
    for location in store_locations:
        loc_latitude = float(location["Latitude"])
        loc_longitude = float(location["Longitude"])
        dist = distance_between_points(
            latitude, longitude, loc_latitude, loc_longitude)
        if dist < distance:
            distance = dist
            nearest = location
    return (nearest, distance)

def fetch_location(address):
    """use geocoder to access latitude and logitude of address given"""
    location = geocoder.osm(address).json
    if location is None:
        raise Exception("Invalid Address provided -> ", address)
    return (location['lat'], location['lng'])

def distance_between_points(latitude1, longitude1, latitude2, longitude2):
    """calculate distance based on the radius of the earth and trignometry"""
    # Computed using the Haversine formula
    # https://en.wikipedia.org/wiki/Haversine_formula
    # translated from https://www.geodatasource.com/developers/javascript
    if latitude1 == latitude2 and longitude1 == longitude2:
        return 0

    rad_latitude1 = math.pi * latitude1/180
    rad_latitude2 = math.pi * latitude2/180
    theta = longitude1 - longitude2
    rad_theta = math.pi * theta/180
    dist = math.sin(rad_latitude1) * math.sin(rad_latitude2) +\
           math.cos(rad_latitude1) * math.cos(rad_latitude2) * math.cos(rad_theta)
    if dist > 1:
      dist = 1
    dist = math.acos(dist);
    dist = dist * 180/math.pi
    dist = dist * 60 * 1.1515
    return dist

def format_store_text(store, distance, units):
    """return the nearest store"""
    return f"""
  Store Name: {store['Store Name']}
  Store Location: {store['Store Location']}
  Address: {store['Address']}
  City: {store['City']}
  State: {store['State']}
  Zip Code: {store['Zip Code']}
  Distance: {distance} {units}.
  """

def format_store_json(store, distance, units):
    """return the json data for storelocations on each store"""
    new_data = {**store}
    new_data["Distance"] = distance
    new_data["Units"] = units
    return json.dumps(new_data)

def handle_options(args):
    address = args.address or args.zipcode
    latitude, longitude = fetch_location(address)
    location, distance = nearest(latitude, longitude, store_locations())
    units = "miles"

    if args.units == "km":
        distance = distance * 1.609344
        units = "km"
    if args.output_format == "json":
        return format_store_json(location, distance, units)
    else:
        return format_store_text(location, distance, units)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, dest="address",
                        help='type the address')

    parser.add_argument('--units', type=str, dest="units", default="mi",
                        help='type the units (mi|km)')

    parser.add_argument('--zip', type=str, dest="zipcode",
                        help='type zip code')

    parser.add_argument('--output', type=str, dest="output_format",
                        help='type the output format (text|json)')

    args = parser.parse_args()

    address = args.address or args.zipcode
    if not address:
        print("Usage:")
        parser.print_help()
        sys.exit(-1)
    print(handle_options(args))


if __name__ == "__main__":
    main()
