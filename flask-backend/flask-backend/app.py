from flask import Flask
from models import db
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (not recommended for production)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
