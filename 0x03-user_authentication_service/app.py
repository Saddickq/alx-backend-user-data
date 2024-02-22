#!/usr/bin/env python3
"""Flask module
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def message():
    """ login route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email=email, password=password):
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout route"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user_id=user.id)
            return redirect(url_for('message'))
    abort(403)


@app.route("/profile")
def profile():
    """GET /profile
        Profile
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return (jsonify({"email": user.email}), 200)
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """POST /reset_password
        Reset Password
    """
    email = request.form.get("email")
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return (jsonify({"email": email, "reset_token": reset_token}), 200)
        except ValueError:
            abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """PUT /reset_password
        Reset Password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return (jsonify({"email": email,
                             "message": "Password updated"}), 200)
        except Exception:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
