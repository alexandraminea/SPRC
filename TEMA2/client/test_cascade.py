import requests

URL = "http://localhost:5000/api/countries"
URL2 = "http://localhost:5000/api/countries/2"
URL1 = "http://localhost:5000/api/countries/1"
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

r = requests.get(URL)
print(r.text)

data = {"country_id" : '1', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

r = requests.get(URL_CITY)
print(r.text)


print("delete 1")
r = requests.delete(URL1)
print(r)

r = requests.get(URL)
print(r.text)


r = requests.get(URL_CITY)
print(r.text)
