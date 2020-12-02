import requests

URL = "http://localhost:5000/api/countries"
URL_CITY = "http://localhost:5000/api/cities"
URL_CITY1 = "http://localhost:5000/api/cities/1"
URL_CITY2 = "http://localhost:5000/api/cities/2"
URL_CITY_CO = "http://localhost:5000/api/cities/country/8"

data = {"name" : "Sweden", "latitude" : '48.90',  "longitude" : '36.44'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "England", "latitude" : '39.5',  "longitude" : '37.99'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "Romania", "latitude" : '44.6',  "longitude" : '25.98'}
r = requests.post(URL, json=data)
print(r)
data = {"country_id" : '2', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '2', "city_name" : "AltOras", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '1', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

print("delete 1")
r = requests.delete(URL_CITY1)
print(r)

print("replace 2")
data = {"country_id" : '1', "city_name" : "ReplacedName", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.put(URL_CITY2, json=data)
print(r)

r = requests.get(URL_CITY)
print(r.text)

data = {"country_id" : '2', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.put(URL_CITY1, json=data)
print(r)

r = requests.get(URL_CITY_CO)
print(r.text)