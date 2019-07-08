## Overview
StoreNearMe finds the nearest store to a location given by the user, using the address and the zip code. This app is built using Python and the GeoCoder library's open street map API. 

The application uses the CSV dict reader to read the file and allows Python to access it.  

The GeoCoder library takes the address or zip code given on the command line and identifies its latitude and longitude. The application takes these coordinates, compares it with the coordinates of the stores in the CSV file.

It then uses the Haversine formula to calculate the distance to the nearest store. The Haversine formula uses trignometry and the radius of the earth's circumferance to find the distance. This is considered to be the best way to to find the distance between two geographical points, though there are other options like the Manhattan distance. 

The application prints out the nearest store, its location, address and zipcode on the command line. It also prints out the distance to the store from the location given,  in miles or, if the user prefers it, in kilometers. 

This application was tested at all points unit unittests. Fake data was used to check whether the nearest store was being returned in the tests, while actual data was used on the command line to check the application's efficacy. Some edge cases like invalid addresses have been accounted for by asking the program to raise exceptions and seek valid addresses.

All external libraries used including GeoCoder were installed using pipenv install. Argparse was used to speak with the command line, while sys and math were directly imported into the file for the various calculations done in the program. JSon was imported and the data can also be read as json on the command line. 


## Example Usage
* Print usage information
```
$ ./find_store.py
Usage:
usage: find_store.py [-h] [--address ADDRESS] [--units UNITS] [--zip ZIPCODE]
                     [--output OUTPUT_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS     type the address
  --units UNITS         type the units (mi|km)
  --zip ZIPCODE         type zip code
  --output OUTPUT_FORMAT type the output format (text|json)

```
*  Find nearest store by address
```
$ ./find_store.py  --address="Market St, Durham, NC"

  Store Name: Durham
  Store Location: SWC Shannon Rd & US Hwy 15-501
  Address: 4037 Durham Chapel Hill Blvd
  City: Durham
  State: NC
  Zip Code: 27707-2516
  Distance: 3.795293160416604 miles
```
* Find nearest store by zipcode
```
$ ./find_store.py  --zip="27612"

  Store Name: Raleigh Hwy 70
  Store Location: SEC US 70 & Lynn Rd
  Address: 4841 Grove Barton Rd
  City: Raleigh
  State: NC
  Zip Code: 27613-1900
  Distance: 2.4922625582760545 miles.
```

* Get the output in json
```
$ ./find_store.py  --zip=27612 --output=json
{"Store Name": "Raleigh Hwy 70", "Store Location": "SEC US 70 & Lynn Rd", "Address": "4841 Grove Barton Rd", "City": "Raleigh", "State": "NC", "Zip Code": "27613-1900", "Latitude": "35.8705975", "Longitude": "-78.7201235", "County": "Wake County", "Distance": 2.4922625582760545, "Units": "miles"}

```
* Get the distance in kilometers
```
$ ./find_store.py  --zip=27612  --units=km

  Store Name: Raleigh Hwy 70
  Store Location: SEC US 70 & Lynn Rd
  Address: 4841 Grove Barton Rd
  City: Raleigh
  State: NC
  Zip Code: 27613-1900
  Distance: 4.010907794586219 km.
```

### Installation and Testing
```
$ pipenv install
$ python find_store_test.py
....
```
 
### Resources
* [geocoder](https://github.com/DenisCarriere/geocoder)
* [haversine formula for distances](https://en.wikipedia.org/wiki/Haversine_formula)
