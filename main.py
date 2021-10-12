# save this as app.py
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():

    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    print(f"argument : {request.args}")
    print(f"body : {request.get_json()}")
    body = "Hello, World!"

    return make_response(body, 200)

@app.route('/users', methods=["GET"])
def getUsers():
    allUsers = {}
    for base, dirs, files in os.walk("users"):
        for index in files:
            file = open("users/" + index, "r")
            data = file.readlines()
            print(data)
            splited = data[0].split('\n')
            allUsers[index] = {"firstName": splited[0], "lastName": data[1]}
            file.close()
    return make_response((allUsers, 200))

@app.route('/users', methods=["POST"])
def addUser():
    body = request.get_json()
    index = request.args["id"]
    firstName = body["firstName"]
    lastName = body["lastName"]
    existed = False

    if os.path.exists("users/" + index + ".txt"):
        print("Le fichier existe deja !")
    else:
        for base, dirs, files in os.walk("users"):
            for id in files:
                file = open("users/" + id, "r")
                data = file.readlines()
                splited = data[0].split('\n')
                if firstName in splited[0] and lastName in data[1]:
                    existed = True
                file.close()
        if existed:
            print("Le user existe deja !")
        else:
            new_file = open("users/" + index + '.txt', 'x')
            for x in body:
                new_file.write(body[x] + "\n")
            new_file.close()
    return make_response((body, 200))


@app.route('/users', methods=["PATCH"])
def updateUser():
    body = request.get_json()
    index = request.args["id"]

    if os.path.exists("users/" + index + ".txt"):
        new_file = open("users/" + index + '.txt', 'w')
        for x in body:
            new_file.write(body[x] + "\n")
        new_file.close()
    else:
        print("Le fichier n'existe pas !")

    return make_response((body, 200))


@app.route('/users', methods=["DELETE"])
def deleteUser():
    index = request.args["id"]
    if os.path.exists("users/" + index + ".txt"):
        os.remove("users/" + index + ".txt")
    else :
        print("Le fichier n'existe pas !")
    return "DELETE"



if __name__ == '__main__':
    app.run(
        host="10.138.34.170",
        #host="192.168.1.48",
        port=8001,
        debug=True,
    )