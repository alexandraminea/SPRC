import requests

URL = "http://localhost:5000/api/countries"
URL2 = "http://localhost:5000/api/countries/2"
URL1 = "http://localhost:5000/api/countries/1"
URL_CITY = "http://localhost:5000/api/cities"

data = {"name" : "Sweden", "latitude" : '48.90',  "longitude" : '36.44'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "England", "latitude" : '39.5',  "longitude" : '37.99'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "Romania", "latitude" : '44.6',  "longitude" : '25.98'}
r = requests.post(URL, json=data)
print(r)

data = {"country_id" : '1', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

# print("delete 2")
# r = requests.delete(URL2)
# print(r)

# r = requests.get(URL)
# print(r.text)

print("replace 1")
data = {"name" : "Romania", "latitude" : '22.22',  "longitude" : '55.56'}
r = requests.put(URL1, json=data)
print(r)

r = requests.get(URL)
print(r.text)