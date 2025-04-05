from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from .. import db, bcrypt
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Validate email
        valid = validate_email(data['email'])
        email = valid.email
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email address'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create new user
    new_user = User(
        email=email,
        password=hashed_password,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        address=data.get('address'),
        role=data.get('role', 'user')
    )
    
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating user'}), 500
    
    # Create access token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': new_user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not bcrypt.check_password_hash(user.password, data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    user.password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating password'}), 500
    
    return jsonify({'message': 'Password updated successfully'}), 200 