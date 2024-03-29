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
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

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


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    it is used to get the profile of the user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = jsonify({'email': user.email})
        return response, 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    generates a password reset token
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return {
                "email": email,
                "reset_token": reset_token
                }, 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    it is used to update the user's password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    parameter_checker = [email, reset_token, new_password]

    if None in parameter_checker:
        abort(400)

    try:
        AUTH.update_password(reset_token, password)
        return {
                "email": email,
                "message": "Password updated"
                }, 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
