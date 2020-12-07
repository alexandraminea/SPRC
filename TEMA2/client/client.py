import requests

URL = "http://localhost:5000/api/countries"
URL_CO1 = "http://localhost:5000/api/countries/1"
URL_CO2 = "http://localhost:5000/api/countries/2"
URL_CO3 = "http://localhost:5000/api/countries/3"
URL_CO_INVALID = "http://localhost:5000/api/countries/10"

URL_CITIES = "http://localhost:5000/api/cities"
URL_CITY1 = "http://localhost:5000/api/cities/1"
URL_CITY2 = "http://localhost:5000/api/cities/2"
URL_CITY6 = "http://localhost:5000/api/cities/6"
URL_CITY3 = "http://localhost:5000/api/cities/3"
URL_CITY_INVALID = "http://localhost:5000/api/cities/20"

URL_CITY_CO = "http://localhost:5000/api/cities/country/1"

URL_T = "http://localhost:5000/api/temperatures"
URL_T1 = "http://localhost:5000/api/temperatures/1"
URL_T2 = "http://localhost:5000/api/temperatures/2"
URL_INVALID_TEMP = "http://localhost:5000/api/temperatures/10"

URL_TCIT1 = "http://localhost:5000/api/temperatures/cities/1"
URL_TCO2 = "http://localhost:5000/api/temperatures/countries/2"


def check_test(expected, got):
    if got == expected:
        print(f"CHECK STATUS {expected} ..................... OK")
    else:
        print(f"EXPECTED {expected} and got {got} ......... NOT OK")

# /api/countries ---------------------------------------------------------------------------

print(" -------------------- Testing /api/countries -------------------- ")
print(" -------------------- POST -------------------")
# POST
# valid entries - 201

data = {"nume" : "Romania", "lat" : '44.439663',  "lon" : '26.096306'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"nume" : "England", "lat" : '51.507351',  "lon" : '-0.127758'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"nume" : "Sweden", "lat" : '59.329323',  "lon" : '18.068581'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"nume" : "Italy", "lat" : '41.871941',  "lon" : '12.567380'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

# bad request - 400
# string latitude
data = {"nume" : "BadLatitude", "lat" : 'abc',  "lon" : '12.567380'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

data = {"nume" : "BadCountry", "lat" : '44.439663'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

# db conflict -> duplicate country name - 409
data = {"nume" : "Romania", "lat" : '44.439663',  "lon" : '26.096306'}
r = requests.post(URL, json=data)
got = r.status_code
expected = 409
check_test(expected=expected, got=got)

print(" -------------------- GET --------------------")
# GET - 200
r = requests.get(URL)
print(r.text)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# /api/countries/idTara ----------------------------------------------------------------------
print()
print(" -------------------- Testing /api/countries/id -------------------- ")

# PUT 
# valid put - 200
print(" -------------------- PUT --------------------")
data = {'id': '1',"nume" : "Romania", "lat" : '59.329324',  "lon" : '18.068582'}
r = requests.put(URL_CO1, json=data)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# bad request - 400
data = {'id': '1', "lat" : '59.329324',  "lon" : '18.068582'}
r = requests.put(URL_CO1, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

data = {'id': '2',"nume" : "Romania", "lat" : '59.329324',  "lon" : '18.068582'}
r = requests.put(URL_CO1, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

# country not found - 404
data = {'id': '10', "nume" : "NoCountry", "lat" : '59.329324',  "lon" : '18.068582'}
r = requests.put(URL_CO_INVALID, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

# db conflict -> duplicate country name - 409
data = {'id': '1', "nume" : "England", "lat" : '51.507351',  "lon" : '-0.127758'}
r = requests.put(URL_CO1, json=data)
got = r.status_code
expected = 409
check_test(expected=expected, got=got)

# DELETE
# valid delete - 200
print(" -------------------- DELETE ----------------- ")
r = requests.delete(URL_CO3)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# country not found - 404
r = requests.delete(URL_CO_INVALID)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

print("deleted Sweden")
r = requests.get(URL)
print(r.text)


# /api/cities ----------------------------------------------------------------------
print()
print(" -------------------- Testing /api/cities -------------------- ")
print(" -------------------- POST -------------------")
# POST
# valid entries - 201

data = {"idTara" : '1', "nume" : "Bucuresti", "lat" : '44.426765',  "lon" : '26.102537'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idTara" : '1', "nume" : "Ploiesti", "lat" : '44.940399',  "lon" : '26.023821'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idTara" : '2', "nume" : "Manchester", "lat" : '53.4723272',  "lon" : '-2.2935022'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idTara" : '2', "nume" : "Liverpool", "lat" : '53.4766108',  "lon" : '-2.257405'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idTara" : '4', "nume" : "Venezia", "lat" : '53.4723272',  "lon" : '12.2472504'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idTara" : '4', "nume" : "Milanoo", "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

# bad request - 400
data = {"idTara" : '4', "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)


# not found 404
data = {"idTara" : '10', "nume" : "BadCity", "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.post(URL_CITIES, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)


print(" -------------------- GET --------------------")
# GET - 200
r = requests.get(URL_CITIES)
print(r.text)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# /api/cities/idOras ----------------------------------------------------------------------
print()
print(" -------------------- Testing /api/cities/idOras -------------------- ")

# PUT
#valid
print(" -------------------- PUT --------------------")
data = {'id': '6', "idTara" : '4', "nume" : "Milano", "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.put(URL_CITY6, json=data)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# bad request - 400
data = {"idTara" : '4', "nume" : "BadCity"}
r = requests.put(URL_CITY1, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

# bad request - 400
data = {'id': '4', "idTara" : '4', "nume" : "Milano", "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.put(URL_CITY6, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)


# city not found - 404
data = {'id': '20',"idTara" : '4', "nume" : "Milano", "lat" : '45.404698',  "lon" : '9.1076927'}
r = requests.put(URL_CITY_INVALID, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

# db conflict -> violating (country_id, city_name) unicity - 409
data = {'id': '2', "idTara" : '1', "nume" : "Bucuresti", "lat" : '44.426765',  "lon" : '26.102537'}
r = requests.put(URL_CITY2, json=data)
got = r.status_code
expected = 409
check_test(expected=expected, got=got)

# DELETE
# valid delete - 200
print(" -------------------- DELETE ----------------- ")
print("delete Manchester")
r = requests.delete(URL_CITY3)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

r = requests.get(URL_CITIES)
print(r.text)

# city not found - 404
r = requests.delete(URL_CITY_INVALID)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

# /api/ cities /country/:idTara ----------------------------------------------------------------------
print()
print(" -------------------- Testing /api/cities/country/idTara-------------------- ")

print(" -------------------- GET --------------------")
print("Cities in Romania")

# POST - 201
r = requests.get(URL_CITY_CO)
print(r.text)

# /api/temperatures ----------------------------------------------------------------------

print()
print(" -------------------- Testing /api/temperatures ---------------------------- ")
print(" -------------------- POST -------------------")

data = {"idOras" : '1', 'valoare' : '23.55'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idOras" : '2', 'valoare' : '27.55'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idOras" : '4', 'valoare' : '-2.3'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idOras" : '5', 'valoare' : '-2.3'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

data = {"idOras" : '6', 'valoare' : '-4.3440'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 201
check_test(expected=expected, got=got)

# db conflict -> violating (city_id, timestamp) unicity - 409
data = {"idOras" : '6', 'valoare' : '44.56'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 409
check_test(expected=expected, got=got)

# bad request - 400
data = {"idOras" : '6'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)


# city/id not found - 404
data = {"idOras" : '3', 'valoare' : '44.56'}
r = requests.post(URL_T, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)


print(" -------------------- GET -------------------")

print("\nGET no params")
r = requests.get(URL_T)
print(r.text)

print("\nGET only by latitude (City)")
params={'lat':'44.426765'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET only by latitude and longitude (City)")
params={'lat':'44.426765', 'lon':'26.102537'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET only by from_date (City)")
params={'from': '2020-12-02'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET only by from_date and until_date (City)")
params={'from': '2020-12-02', 'until':'2020-12-05'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET by all params (City)")
params={'lat':'44.426765', 'lon':'26.102537', 'from': '2020-12-02', 'until':'2020-12-05'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET by all params (Country)")
params={"lat" : '44.426765',  "lon" : '26.102537', 'from': '2020-12-02', 'until':'2020-12-09'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET no lat/lon match (City)")
params={"lat" : '44',  "lon" : '26', 'from': '2020-12-02', 'until':'2020-12-09'}
r = requests.get(URL_T, params=params)
print(r.text)

print("\nGET no date match (City)")
params={"lat" : '44',  "lon" : '26', 'from': '2021-12-02', 'until':'2021-12-09'}
r = requests.get(URL_T, params=params)
print(r.text)


print()
print(" -------------------- Testing /api/temperatures/id ---------------------------- ")

print(" -------------------- PUT --------------------")
data = {'id': '1', "idOras" : '1', 'valoare' : '44.5644'}
r = requests.put(URL_T1, json=data)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

# bad request - 400
data = {'id': '1', 'valoare' : '44.5644'}
r = requests.put(URL_T1, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

data = {'id': '2', "idOras" : '1', 'valoare' : '44.5644'}
r = requests.put(URL_T1, json=data)
got = r.status_code
expected = 400
check_test(expected=expected, got=got)

# city/id not found - 404
data = {'id': '10', "idOras" : '1', 'valoare' : '44.5644'}
r = requests.put(URL_INVALID_TEMP, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

data = {'id': '1', "idOras" : '20', 'valoare' : '44.5644'}
r = requests.put(URL_T1, json=data)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)

# db conflict -> violating (city_id, timestamp) unicity - 409
data = {'id': '1', "idOras" : '6', 'valoare' : '44.56'}
r = requests.put(URL_T1, json=data)
got = r.status_code
expected = 409
check_test(expected=expected, got=got)

print(" -------------------- DELETE ----------------- ")
print("delete second temperature")
r = requests.delete(URL_T2)
got = r.status_code
expected = 200
check_test(expected=expected, got=got)

r = requests.get(URL_T)
print(r.text)

# temp not found - 404
r = requests.delete(URL_INVALID_TEMP)
got = r.status_code
expected = 404
check_test(expected=expected, got=got)


print("-------- GET /api/temperatures/cities/idOras -----------")

print("\nGET only by until_date")
params={'until':'2020-12-03'}

r = requests.get(URL_TCIT1, params=params)
print(r.text)

print("------- GET /api/temperatures/countries/idTara ----------")

print("\nGET by from_date and until_date")
params={'from': '2020-12-01','until':'2020-12-03'}

r = requests.get(URL_TCO2, params=params)
print(r.text)


print("\n------- TEST remove City cascade ----------")
print("Remove City 1 => no temperature entries for City 1")
r = requests.delete(URL_CITY1)
r = requests.get(URL_TCIT1, params=params)
print(r.text)

print("\n------- TEST remove Country cascade ----------")
print("Remove Country 2 => no temperature entries for Country 2")
r = requests.delete(URL_CO2)
r = requests.get(URL_TCO2, params=params)
print(r.text)