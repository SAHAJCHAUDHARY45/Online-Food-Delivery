from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.restaurant import Restaurant
from ..models.menu_item import MenuItem
from ..models.user import User
from .. import db
from datetime import datetime

restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/', methods=['GET'])
def get_restaurants():
    # Get query parameters
    cuisine_type = request.args.get('cuisine_type')
    rating = request.args.get('rating')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Base query
    query = Restaurant.query.filter_by(is_active=True)
    
    # Apply filters
    if cuisine_type:
        query = query.filter_by(cuisine_type=cuisine_type)
    if rating:
        query = query.filter(Restaurant.reviews.any(rating=rating))
    if search:
        query = query.filter(Restaurant.name.ilike(f'%{search}%'))
    
    # Paginate results
    restaurants = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'restaurants': [restaurant.to_dict() for restaurant in restaurants.items],
        'total': restaurants.total,
        'pages': restaurants.pages,
        'current_page': restaurants.page
    }), 200

@restaurant_bp.route('/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return jsonify(restaurant.to_dict()), 200

@restaurant_bp.route('/', methods=['POST'])
@jwt_required()
def create_restaurant():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role not in ['admin', 'restaurant_owner']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'address', 'phone', 'cuisine_type']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_restaurant = Restaurant(
        name=data['name'],
        description=data.get('description'),
        address=data['address'],
        phone=data['phone'],
        cuisine_type=data['cuisine_type'],
        opening_time=datetime.strptime(data['opening_time'], '%H:%M').time() if 'opening_time' in data else None,
        closing_time=datetime.strptime(data['closing_time'], '%H:%M').time() if 'closing_time' in data else None,
        image_url=data.get('image_url'),
        delivery_fee=data.get('delivery_fee', 0.0),
        minimum_order=data.get('minimum_order', 0.0),
        owner_id=user_id
    )
    
    db.session.add(new_restaurant)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating restaurant'}), 500
    
    return jsonify(new_restaurant.to_dict()), 201

@restaurant_bp.route('/<int:restaurant_id>', methods=['PUT'])
@jwt_required()
def update_restaurant(restaurant_id):
    user_id = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Check if user is owner or admin
    if restaurant.owner_id != user_id and User.query.get(user_id).role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    for field in ['name', 'description', 'address', 'phone', 'cuisine_type', 'image_url', 
                 'delivery_fee', 'minimum_order', 'is_active']:
        if field in data:
            setattr(restaurant, field, data[field])
    
    # Update times if provided
    if 'opening_time' in data:
        restaurant.opening_time = datetime.strptime(data['opening_time'], '%H:%M').time()
    if 'closing_time' in data:
        restaurant.closing_time = datetime.strptime(data['closing_time'], '%H:%M').time()
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating restaurant'}), 500
    
    return jsonify(restaurant.to_dict()), 200

@restaurant_bp.route('/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id, is_available=True).all()
    return jsonify([item.to_dict() for item in menu_items]), 200

@restaurant_bp.route('/<int:restaurant_id>/menu', methods=['POST'])
@jwt_required()
def add_menu_item(restaurant_id):
    user_id = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Check if user is owner or admin
    if restaurant.owner_id != user_id and User.query.get(user_id).role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_item = MenuItem(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('image_url'),
        category=data.get('category'),
        is_vegetarian=data.get('is_vegetarian', False),
        is_vegan=data.get('is_vegan', False),
        is_gluten_free=data.get('is_gluten_free', False),
        spice_level=data.get('spice_level', 0),
        restaurant_id=restaurant_id
    )
    
    db.session.add(new_item)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating menu item'}), 500
    
    return jsonify(new_item.to_dict()), 201

@restaurant_bp.route('/<int:restaurant_id>/menu/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_menu_item(restaurant_id, item_id):
    user_id = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_item = MenuItem.query.get_or_404(item_id)
    
    # Check if item belongs to restaurant
    if menu_item.restaurant_id != restaurant_id:
        return jsonify({'error': 'Item not found in restaurant'}), 404
    
    # Check if user is owner or admin
    if restaurant.owner_id != user_id and User.query.get(user_id).role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    for field in ['name', 'description', 'price', 'image_url', 'category', 
                 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'spice_level', 'is_available']:
        if field in data:
            setattr(menu_item, field, data[field])
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating menu item'}), 500
    
    return jsonify(menu_item.to_dict()), 200

@restaurant_bp.route('/<int:restaurant_id>/menu/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(restaurant_id, item_id):
    user_id = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_item = MenuItem.query.get_or_404(item_id)
    
    # Check if item belongs to restaurant
    if menu_item.restaurant_id != restaurant_id:
        return jsonify({'error': 'Item not found in restaurant'}), 404
    
    # Check if user is owner or admin
    if restaurant.owner_id != user_id and User.query.get(user_id).role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(menu_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error deleting menu item'}), 500
    
    return jsonify({'message': 'Menu item deleted successfully'}), 200 