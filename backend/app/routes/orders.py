from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.order import Order, OrderItem
from ..models.restaurant import Restaurant
from ..models.menu_item import MenuItem
from ..models.user import User
from .. import db
from datetime import datetime, timedelta

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['restaurant_id', 'items', 'delivery_address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if restaurant exists and is active
    restaurant = Restaurant.query.get_or_404(data['restaurant_id'])
    if not restaurant.is_active:
        return jsonify({'error': 'Restaurant is not available'}), 400
    
    # Calculate total amount and validate items
    total_amount = 0
    order_items = []
    
    for item_data in data['items']:
        if 'menu_item_id' not in item_data or 'quantity' not in item_data:
            return jsonify({'error': 'Invalid item data'}), 400
        
        menu_item = MenuItem.query.get_or_404(item_data['menu_item_id'])
        if menu_item.restaurant_id != restaurant.id:
            return jsonify({'error': 'Item does not belong to restaurant'}), 400
        if not menu_item.is_available:
            return jsonify({'error': f'Item {menu_item.name} is not available'}), 400
        
        item_total = menu_item.price * item_data['quantity']
        total_amount += item_total
        
        order_items.append({
            'menu_item': menu_item,
            'quantity': item_data['quantity'],
            'price': menu_item.price,
            'special_instructions': item_data.get('special_instructions')
        })
    
    # Check minimum order amount
    if total_amount < restaurant.minimum_order:
        return jsonify({
            'error': f'Minimum order amount is ${restaurant.minimum_order}'
        }), 400
    
    # Add delivery fee
    total_amount += restaurant.delivery_fee
    
    # Create order
    new_order = Order(
        user_id=user_id,
        restaurant_id=restaurant.id,
        total_amount=total_amount,
        delivery_fee=restaurant.delivery_fee,
        delivery_address=data['delivery_address'],
        delivery_instructions=data.get('delivery_instructions'),
        payment_method=data.get('payment_method', 'card'),
        estimated_delivery_time=datetime.utcnow() + timedelta(minutes=45)
    )
    
    # Add order items
    for item in order_items:
        order_item = OrderItem(
            menu_item_id=item['menu_item'].id,
            quantity=item['quantity'],
            price=item['price'],
            special_instructions=item['special_instructions']
        )
        new_order.items.append(order_item)
    
    db.session.add(new_order)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating order'}), 500
    
    return jsonify(new_order.to_dict()), 201

@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get query parameters
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Base query
    if user.role == 'admin':
        query = Order.query
    elif user.role == 'restaurant_owner':
        query = Order.query.filter_by(restaurant_id=user.restaurant.id)
    else:
        query = Order.query.filter_by(user_id=user_id)
    
    # Apply status filter
    if status:
        query = query.filter_by(status=status)
    
    # Sort by creation date, newest first
    query = query.order_by(Order.created_at.desc())
    
    # Paginate results
    orders = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order.to_dict() for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': orders.page
    }), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to view order
    if user.role != 'admin' and order.user_id != user_id and \
       (user.role != 'restaurant_owner' or order.restaurant_id != user.restaurant.id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(order.to_dict()), 200

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to update order
    if user.role != 'admin' and \
       (user.role != 'restaurant_owner' or order.restaurant_id != user.restaurant.id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': 'Missing status field'}), 400
    
    valid_statuses = ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    order.status = data['status']
    if data['status'] == 'delivered':
        order.actual_delivery_time = datetime.utcnow()
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating order status'}), 500
    
    return jsonify(order.to_dict()), 200

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns the order
    if order.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Check if order can be cancelled
    if order.status not in ['pending', 'confirmed']:
        return jsonify({'error': 'Order cannot be cancelled'}), 400
    
    order.status = 'cancelled'
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error cancelling order'}), 500
    
    return jsonify(order.to_dict()), 200 