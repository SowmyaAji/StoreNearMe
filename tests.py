import unittest
import find_store
import json

class TestFindStoreMethods(unittest.TestCase):
    def test_nearest(self):
        store1 = dict(Latitude=100, Longitude=100)
        store2 = dict(Latitude=102, Longitude=102)
        self.assertEqual((store1, 0), find_store.nearest(
            store1["Latitude"], store1["Longitude"], [store1, store2]))

        store3 = dict(Latitude="200", Longitude="200")
        self.assertEqual((store1, 0), find_store.nearest(
            store1["Latitude"], store1["Longitude"], [store1, store2, store3]))

    def test_distance_points(self):
        self.assertEqual(0, find_store.distance_between_points(1, 1, 1, 1))
        self.assertEqual(
            True, find_store.distance_between_points(1, 1, 4, 4) > 0)

    def test_format_store_text(self):
        store1 = {
            "Store Name": "foo",
            "Store Location": "100 sddfoo",
            "Address": "22939 foo",
            "City": "foo",
            "State":"nc",
            "Zip Code": "44444",
            "Latitude": 100,
            "Longitude": 100
        }

        distance = 1000
        actual = find_store.format_store_text(store1, distance,"km")
        self.assertEqual(True, actual.find("Store Name: foo") > -1 )
        self.assertEqual(True, actual.find("Store Location: 100 sddfoo") > -1 )
        self.assertEqual(True, actual.find("Zip Code: 44444") > -1 )
        self.assertEqual(True, actual.find("Distance: 1000 km") > -1 )

        actual = find_store.format_store_text(store1, distance,"miles")
        self.assertEqual(True, actual.find("Distance: 1000 miles") > -1 )

    def test_format_store_json(self):
        store1 = {
            "Store Name": "foo",
            "Store Location": "100 sddfoo",
            "Address": "22939 foo",
            "City": "foo",
            "State":"nc",
            "Zip Code": "44444",
            "Latitude": 100,
            "Longitude": 100
        }

        distance = 1000
        actual = json.loads(find_store.format_store_json(store1, distance,"km"))
        for key in store1.keys():
            self.assertEqual(store1[key], actual[key])  

        self.assertEqual(distance, actual["Distance"])
        self.assertEqual("km", actual["Units"])

        actual = json.loads(find_store.format_store_json(store1, distance,"miles"))
        self.assertEqual("miles", actual["Units"])

if __name__ == '__main__':
    unittest.main()
