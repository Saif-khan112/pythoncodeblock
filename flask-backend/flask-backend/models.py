from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON

db = SQLAlchemy()
bcrypt = Bcrypt()

story_products = db.Table(
    'story_products',
    db.Column('story_id', db.Integer, db.ForeignKey('stories.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_api_key = db.Column(db.String(200))
    store_domain = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    photo_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StoryType(Enum):
    Shoppable = 'shoppable'
    CTA = 'cta'

# class Stories(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     type = db.Column(db.Enum('shoppable', 'cta', name='story_type'), nullable=False)
#     product_ids = db.Column(JSON, nullable=True)  # For shoppable stories
#     cta_text = db.Column(db.String(255), nullable=True)  # For CTA stories
#     cta_link = db.Column(db.String(255), nullable=True)  # For CTA stories
#     video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)  # Linked video
#     created_at = db.Column(db.DateTime, default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.Enum('shoppable', 'cta', name='story_type'), nullable=False)
    cta_text = db.Column(db.String(255), nullable=True)
    cta_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relationships
    products = db.relationship(
        'Product', 
        secondary=story_products,
        backref=db.backref('stories', lazy='dynamic'),
        lazy='dynamic',
        primaryjoin="Stories.id == story_products.c.story_id", 
        secondaryjoin="Product.id == story_products.c.product_id"
    )

    # Relationship to Video (Change backref to something unique)
    # video = db.relationship('Video', backref=db.backref('videos_for_story', lazy=True),  uselist=False )
    video = db.relationship('Video', backref='stories', uselist=False)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=True)  # Foreign Key to Stories
    # video_url = db.Column(db.String(200))
    mux_playback_id = db.Column(db.String(100))
    # Relationship to Stories
    story = db.relationship('Stories', backref=db.backref('videos', lazy=True))




# class Bubble(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
#     size = db.Column(db.Integer)
#     order = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Bubble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('BubbleItem', backref='bubble', cascade="all, delete-orphan")


class BubbleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bubble_id = db.Column(db.Integer, db.ForeignKey('bubble.id', ondelete="CASCADE"), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id', ondelete="SET NULL"), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    story = db.relationship('Stories', backref='bubble_items')
