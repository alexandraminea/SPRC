import requests

URL_T = "http://localhost:5000/api/temperatures"
URL_CITY = "http://localhost:5000/api/cities"
URL = "http://localhost:5000/api/countries"
URL_T1 = "http://localhost:5000/api/temperatures/cities/1"
URL_TC1 = "http://localhost:5000/api/temperatures/countries/1"

# add countries

data = {"name" : "Romania", "latitude" : '48.90',  "longitude" : '36.44'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "Sweden", "latitude" : '48.67',  "longitude" : '55.789'}
r = requests.post(URL, json=data)
print(r)

data = {"name" : "England", "latitude" : '65.67',  "longitude" : '45.56'}
r = requests.post(URL, json=data)
print(r)

# add cities

data = {"country_id" : '1', "city_name" : "Bucuresti", "latitude" : '23.77',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '1', "city_name" : "Ploiesti", "latitude" : '23.77',  "longitude" : '33.44'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '2', "city_name" : "Vaxholm", "latitude" : '22.87',  "longitude" : '44.98'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '2', "city_name" : "Stockholm", "latitude" : '55.67',  "longitude" : '33.44'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '2', "city_name" : "London", "latitude" : '23.77',  "longitude" : '32.89'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '2', "city_name" : "Oxford", "latitude" : '21.98',  "longitude" : '34.77'}
r = requests.post(URL_CITY, json=data)
print(r)

data = {"country_id" : '3', "city_name" : "Mancester", "latitude" : '48.90',  "longitude" : '34.77'}
r = requests.post(URL_CITY, json=data)
print(r)
r = requests.get(URL_CITY)
print(r.text)

# add temperatures

data = {"city_id" : '1', 'value' : '23.55'}
r = requests.post(URL_T, json=data)
print(r)

data = {"city_id" : '2', 'value' : '27.55'}
r = requests.post(URL_T, json=data)
print(r)

data = {"city_id" : '3', 'value' : '44.56'}
r = requests.post(URL_T, json=data)
print(r)

data = {"city_id" : '4', 'value' : '-2.3'}
r = requests.post(URL_T, json=data)
print(r)

data = {"city_id" : '5', 'value' : '-2.3'}
r = requests.post(URL_T, json=data)
print(r)

data = {"city_id" : '7', 'value' : '-4.3440'}
r = requests.post(URL_T, json=data)
print(r)

params={'lat':'23.770'}
params={'lon':'44.98'}
params={'lat':'48.90'}
params={'until':'2020-12-02'}

r = requests.get(URL_TC1, params=params)
print(r.text)