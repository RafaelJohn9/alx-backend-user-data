#!/usr/bin/env python3
"""
A flask app that has a single  GET route '/'
and use flask.jsonify to return a JSON payload of the form
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def home():
    """
    provides a welcome message as the root to api
    """
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    used  in user login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        AUTH.create_session(email)
        return {"email": email, "message": "logged in"}

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    it is used to delete the user session
    and logs out
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect(url_for('home'))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
