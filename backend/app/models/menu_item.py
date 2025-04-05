from .. import db
from datetime import datetime

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50))
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)
    spice_level = db.Column(db.Integer, default=0)  # 0-4: None to Extra Spicy
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'is_vegetarian': self.is_vegetarian,
            'is_vegan': self.is_vegan,
            'is_gluten_free': self.is_gluten_free,
            'spice_level': self.spice_level,
            'is_available': self.is_available,
            'restaurant_id': self.restaurant_id
        } 