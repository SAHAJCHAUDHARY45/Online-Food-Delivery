from .. import db
from datetime import datetime

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at the time of order
    special_instructions = db.Column(db.Text)
    
    menu_item = db.relationship('MenuItem')
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_item': self.menu_item.to_dict(),
            'quantity': self.quantity,
            'price': self.price,
            'special_instructions': self.special_instructions
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, default=0.0)
    delivery_address = db.Column(db.String(200), nullable=False)
    delivery_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_delivery_time = db.Column(db.DateTime)
    actual_delivery_time = db.Column(db.DateTime)
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    payment_method = db.Column(db.String(50))
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'delivery_fee': self.delivery_fee,
            'delivery_address': self.delivery_address,
            'delivery_instructions': self.delivery_instructions,
            'created_at': self.created_at.isoformat(),
            'estimated_delivery_time': self.estimated_delivery_time.isoformat() if self.estimated_delivery_time else None,
            'actual_delivery_time': self.actual_delivery_time.isoformat() if self.actual_delivery_time else None,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'items': [item.to_dict() for item in self.items]
        } 