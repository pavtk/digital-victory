from flask import Blueprint, jsonify, render_template, request
from .models import User
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'Invalid JSON'}), 400
    if not user_data.get('name') or not user_data.get('email'):
        return jsonify({"error": "Имя и Email не могут быть пустыми"}), 400

    user = User(name=user_data['name'], email=user_data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route('/users')
def get_users():
    return jsonify([u.to_dict() for u in User.query.all()])


@bp.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())