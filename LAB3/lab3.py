from flask import Flask, json, Response, request

app = Flask(__name__)

movies = {}
count = 0

def check_json(movie):
    if movie and "nume" in movie:
        return True
    return False

@app.route("/movies", methods=["GET", "POST"])

def get_response():
    global movies, count
    if request.method == "GET":
        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps(movies)
        )
    elif request.method == "POST":
        movie = request.json
        if check_json(movie):
            movies[count] = movie
            count += 1
            return Response(status=201, response="CREATED")
        else:
            return Response(status=400)

@app.route("/movies/<id>", methods=["GET", "PUT", "DELETE"])

def response(id):
    global movies, count
    if int(id) not in movies:
        return Response(status=404)
    elif request.method == "GET":      
        movie = movies[int(id)]
        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps(movie)
        )
    elif request.method == "PUT":
        movie = request.json
        if check_json(movie):
            movies[int(id)] = movie
            return Response(status=200)
        else:
            return Response(status=400)
    elif request.method == "DELETE":
        print(movies[int(id)])
        del(movies[int(id)])
        return Response(status=400)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)