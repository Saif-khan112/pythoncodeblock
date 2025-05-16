from app import create_app
from routes.auth import auth_bp
from routes.settings import settings_bp
from routes.product import product_bp
from routes.stories import stories_bp
from routes.video import video_bp
from routes.bubble import bubbles_bp
from models import db

app = create_app()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(settings_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(stories_bp, url_prefix='/api')
app.register_blueprint(video_bp, url_prefix='/api')
app.register_blueprint(bubbles_bp, url_prefix='/api')

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
