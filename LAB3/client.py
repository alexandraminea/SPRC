import requests

URL = "http://localhost:5000/movies"
URL2 = "http://localhost:5000/movies/0"

print("add film1")
data = {"nume" : "Film12"}
r = requests.post(URL, json=data)
print(r)

print("add film2")
data = {"nume" : "Film10"}
r = requests.post(URL, json=data)
print(r)

print("get 1")
r = requests.get(URL2)
print(r)

print("get all")
r = requests.get(URL)
print(r.text)

print("replace 1")
data = {"nume" : "FilmNou"}
r = requests.put(URL2, json=data)
print(r)

print("delete 1")
r = requests.delete(URL2)
print(r)

r = requests.get(URL)
print(r.text)