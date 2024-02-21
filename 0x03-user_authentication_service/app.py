#!/usr/bin/env python3
"""
A flask app that has a single  GET route '/'
and use flask.jsonify to return a JSON payload of the form
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    it is used to register a new user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email, password)
        return {"email": email, "message": "user created"}
    except ValueError:
        return {'message': 'email already registered'}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
