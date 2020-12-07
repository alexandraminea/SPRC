from flask import Flask, json, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.sql import func
import json
import requests
import sys
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db:3306/countries_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Country(db.Model):
    __tablename__ = "Country"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.String(10), nullable=False)
    longitude = db.Column(db.String(10), nullable=False)

    def __init__(self, country_name, latitude, longitude):
        self.country_name = country_name
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {'id':self.id, 
                'nume':self.country_name,
                'lat':float(self.latitude),
                'lon':float(self.longitude)}


class City(db.Model):
    __tablename__ = "City"
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.String(10), nullable=False)
    longitude = db.Column(db.String(10), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id', ondelete='CASCADE'), nullable=False)
    db.UniqueConstraint('city_name', 'country_id')

    def __init__(self, city_name, latitude, longitude, country_id):
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude
        self.country_id = country_id

    def to_json(self):
        return {'id':int(self.id), 
                'idTara':self.country_id,
                'nume':self.city_name,
                'lat':float(self.latitude),
                'lon':float(self.longitude)}

    def to_json2(self):
        return {'id':int(self.id),
                'nume':self.city_name,
                'lat':float(self.latitude),
                'lon':float(self.longitude)}

class Temperature(db.Model):
    __tablename__ = "Temperature"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(10))
    ts = db.Column(db.DateTime(timezone=True), server_default=func.now())
    city_id = db.Column(db.Integer, db.ForeignKey('City.id', ondelete='CASCADE'), nullable=False)
    db.UniqueConstraint('value', 'city_id')

    def __init__(self, value, city_id):
        self.value = value
        self.city_id = city_id

    def to_json(self):
        return {'id':int(self.id), 
                'idOras':self.city_id,
                'valoare':float(self.value),
                'timestamp':str(self.ts)}


def check_country(country):
    if country  and "nume" in country \
                and "lat" in country \
                and "lon" in country:
        try:
            float(country["lat"])
            float(country["lon"])
            return True
        except ValueError:
            return False
    return False

def check_city(city):
    if city  and "idTara" in city \
                and "nume" in city \
                and "lat" in city \
                and "lon" in city:
        try:
            float(city["lat"])
            float(city["lon"])
            int(city["idTara"])
            return True
        except ValueError:
            return False
    return False

def check_temp(temp):
    if temp  and "idOras" in temp \
                and "valoare" in temp:
        try:
            int(temp["idOras"])
            float(temp["valoare"])
            return True
        except ValueError:
            return False
    return False
    
def check_id(id):
    try:
        int(id)
        return True
    except ValueError:
        return False


@app.route("/")
def index():
    return "Tare"

@app.route('/api')

@app.route('/api/countries', methods=["GET", "POST"])
def countries_op():
    if request.method == "POST":
        resp = request.json
        if(check_country(resp)):
            try:
                country = Country(
                    country_name = resp["nume"],
                    latitude = resp["lat"],
                    longitude = resp["lon"],
                )
                db.session.add(country)
                db.session.commit()
            except exc.SQLAlchemyError:
                return Response(status=409)
            return Response(status=201)
        else:
            return Response(status=400)
    elif request.method == "GET":
        countries = Country.query.all()
        resp = [country.to_json() for country in countries]
        return Response(status=200,
            mimetype="application/json",
            response=json.dumps(resp)
        )

@app.route("/api/countries/<id>", methods=["PUT", "DELETE"])
def countries_id_op(id):
    if request.method == "PUT":
        resp = request.json
        if(check_country(resp)):
            if not resp["id"] or resp["id"] != id or check_id(resp["id"]) == False:
                return Response(status=400)
            country = Country.query.filter_by(id=id).first()
            try:
                country.country_name = resp["nume"]
                country.latitude = resp["lat"]
                country.longitude = resp["lon"]
            except AttributeError:
                return Response(status=404)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return Response(status=409)
            return Response(status=200)
        else:
            return Response(status=400)
    elif request.method == "DELETE":
        try:
            country = Country.query.filter_by(id=id).first()
            db.session.delete(country)
            db.session.commit()
        except exc.SQLAlchemyError:
                return Response(status=404)
        return Response(status=200)

@app.route('/api/cities', methods=["GET", "POST"])
def cities_op():
    if request.method == "POST":
        resp = request.json
        if(check_city(resp)):
            country = Country.query.filter_by(id=resp['idTara']).first()
            if not country:
                return Response(status=404)
            try:
                city = City(
                    country_id = int(resp["idTara"]),
                    city_name = resp["nume"],
                    latitude = resp["lat"],
                    longitude = resp["lon"],
                )
                db.session.add(city)
                db.session.commit()
            except exc.SQLAlchemyError:
                return Response(status=409)
            return Response(status=201)
        else:
            return Response(status=400)
    elif request.method == "GET":
        cities = City.query.all()
        resp = [city.to_json() for city in cities]
        return Response(status=200,
            mimetype="application/json",
            response=json.dumps(resp)
        )

@app.route("/api/cities/<id>", methods=["PUT", "DELETE"])
def cities_id_op(id):
    if request.method == "PUT":
        resp = request.json
        if(check_city(resp)):
            if not resp["id"] or resp["id"] != id or check_id(resp["id"]) == False:
                return Response(status=400)
            city = City.query.filter_by(id=id).first()
            try:
                city.country_id = int(resp["idTara"])
                city.city_name = resp["nume"]
                city.latitude = resp["lat"]
                city.longitude = resp["lon"]
            except AttributeError:
                return Response(status=404)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return Response(status=409)
            return Response(status=200)
        else:
            return Response(status=400)
    elif request.method == "DELETE":
        try:
            city = City.query.filter_by(id=id).first()
            db.session.delete(city)
            db.session.commit()
        except exc.SQLAlchemyError:
                return Response(status=404)
        return Response(status=200)

@app.route("/api/cities/country/<country_id>", methods=["GET"])
def get_city(country_id):
    if request.method == "GET":
        cities = City.query.filter_by(country_id=country_id)
        resp = [city.to_json2() for city in cities]
        return Response(status=200,
            mimetype="application/json",
            response=json.dumps(resp)
        )

@app.route('/api/temperatures', methods=["POST"])
def post_temperature():
    resp = request.json
    city = City.query.filter_by(id=resp['idOras']).first()
    if not city:
        return Response(status=404)
    if(check_temp(resp)):
        try:
            temp = Temperature(
                value = float(resp["valoare"]),
                city_id = int(resp["idOras"]),
            )
            db.session.add(temp)
            db.session.commit()
        except exc.SQLAlchemyError:
            return Response(status=409)
        return Response(status=201)
    else:
        return Response(status=400)

@app.route('/api/temperatures', methods=["GET"])
def get_temperature():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    from_date = request.args.get('from')
    to_date = request.args.get('until')
    
    if (latitude is None and longitude is None and from_date is None and to_date is None):
        temps = Temperature.query.all()
        resp = [temp.to_json() for temp in temps]
        return Response(status=200,
            mimetype="application/json",
            response=json.dumps(resp)
        )

    queries = []
    if latitude:
        queries.append(City.latitude.cast(db.Float) == float(latitude))
    if longitude:
        queries.append(City.longitude.cast(db.Float) == float(longitude))
    if from_date:
        queries.append(Temperature.ts >= datetime.datetime.strptime(from_date, '%Y-%m-%d'))
    if to_date:
        queries.append(Temperature.ts <= datetime.datetime.strptime(to_date, '%Y-%m-%d'))

    temperatures = db.session.query(Temperature). \
        join(City, Temperature.city_id==City.id). \
        filter(*queries). \
        all()

    queries = []
    if latitude:
        queries.append(Country.latitude.cast(db.Float) == float(latitude))
    if longitude:
        queries.append(Country.longitude.cast(db.Float) == float(longitude))

    temps = db.session.query(Temperature). \
        join(City, Temperature.city_id==City.id). \
        join(Country, City.country_id==Country.id). \
        filter(*queries). \
        all()
    
    resp = [temp.to_json() for temp in temperatures]
    resp += [temp.to_json() for temp in temps]
    resp2 = [i for n, i in enumerate(resp) if i not in resp[n + 1:]]
    return Response(status=200,
        mimetype="application/json",
        response=json.dumps(resp2)
    )

@app.route("/api/temperatures/<id>", methods=["PUT", "DELETE"])
def temp_id_op(id):
    if request.method == "PUT":
        resp = request.json
        if(check_temp(resp)):
            if not resp["id"] or resp["id"] != id or check_id(resp["id"]) == False:
                return Response(status=400)
            city = City.query.filter_by(id=resp['idOras']).first()
            if not city:
                return Response(status=404)
            temp = Temperature.query.filter_by(id=id).first()
            try:
                temp.city_id = int(resp["idOras"]),
                temp.value = float(resp["valoare"]),
            except AttributeError:
                return Response(status=404)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return Response(status=409)
            return Response(status=200)
        else:
            return Response(status=400)
    elif request.method == "DELETE":
        try:
            temp = Temperature.query.filter_by(id=id).first()
            db.session.delete(temp)
            db.session.commit()
        except exc.SQLAlchemyError:
                return Response(status=404)
        return Response(status=200)

@app.route("/api/temperatures/cities/<city_id>", methods=["GET"])
def get_temp_city(city_id):
    from_date = request.args.get('from')
    to_date = request.args.get('until')

    queries = []
    queries.append(Temperature.city_id == city_id)

    if from_date:
        queries.append(Temperature.ts >= datetime.datetime.strptime(from_date, '%Y-%m-%d'))
    if to_date:
        queries.append(Temperature.ts <= datetime.datetime.strptime(to_date, '%Y-%m-%d'))

    temperatures = db.session.query(Temperature). \
        filter(*queries). \
        all()
    
    resp = [temp.to_json() for temp in temperatures]
    return Response(status=200,
        mimetype="application/json",
        response=json.dumps(resp)   
    )

@app.route("/api/temperatures/countries/<country_id>", methods=["GET"])
def get_temp_country(country_id):
    from_date = request.args.get('from')
    to_date = request.args.get('until')

    queries = []
    queries.append(City.country_id == country_id)
    if from_date:
        queries.append(Temperature.ts >= datetime.datetime.strptime(from_date, '%Y-%m-%d'))
    if to_date:
        queries.append(Temperature.ts <= datetime.datetime.strptime(to_date, '%Y-%m-%d'))


    temperatures = db.session.query(Temperature). \
        join(City, Temperature.city_id==City.id). \
        join(Country, City.country_id==Country.id). \
        filter(*queries). \
        all()
    
    resp = [temp.to_json() for temp in temperatures]
    return Response(status=200,
        mimetype="application/json",
        response=json.dumps(resp)
    )

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)