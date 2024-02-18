#!/usr/bin/env python3
""" Module of Users views
"""
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Session authentication."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 400

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return response
