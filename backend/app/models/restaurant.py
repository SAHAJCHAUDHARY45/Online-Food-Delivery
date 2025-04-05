from .. import db
from datetime import datetime

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    cuisine_type = db.Column(db.String(50))
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    image_url = db.Column(db.String(200))
    delivery_fee = db.Column(db.Float, default=0.0)
    minimum_order = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True)
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'cuisine_type': self.cuisine_type,
            'opening_time': self.opening_time.strftime('%H:%M') if self.opening_time else None,
            'closing_time': self.closing_time.strftime('%H:%M') if self.closing_time else None,
            'image_url': self.image_url,
            'delivery_fee': self.delivery_fee,
            'minimum_order': self.minimum_order,
            'is_active': self.is_active,
            'rating': self.average_rating()
        }
    
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews) 