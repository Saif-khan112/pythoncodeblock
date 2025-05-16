# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
# from models import db, Settings
# from schemas import SettingsSchema

# settings_bp = Blueprint('settings', __name__)
# settings_schema = SettingsSchema()
# settings_list_schema = SettingsSchema(many=True)

# # Get all settings
# @settings_bp.route('/settings', methods=['GET'])
# @jwt_required()
# def get_settings():
#     settings = Settings.query.all()
#     return jsonify(settings_list_schema.dump(settings)), 200

# # Create a new setting
# @settings_bp.route('/settings', methods=['POST'])
# @jwt_required()
# def create_setting():
#     data = request.get_json()
#     setting = Settings(**data)
#     db.session.add(setting)
#     db.session.commit()
#     return jsonify(settings_schema.dump(setting)), 201

# --------- 1st one --------------------

# from flask import Blueprint, request, jsonify
# from models import db, Settings
# from flask_jwt_extended import jwt_required

# settings_bp = Blueprint('settings', __name__)

# @settings_bp.route('/settings', methods=['GET'])
# @jwt_required()
# def get_settings():
#     settings = Settings.query.first()
#     if settings:
#         return jsonify({
#             "admin_api_key": settings.admin_api_key,
#             "store_domain": settings.store_domain
#         }), 200
#     return jsonify({"message": "Settings not found"}), 404

# @settings_bp.route('/settings', methods=['POST'])
# @jwt_required()
# def create_settings():
#     data = request.get_json()
#     settings = Settings(admin_api_key=data['admin_api_key'], store_domain=data['store_domain'])
#     db.session.add(settings)
#     db.session.commit()
#     return jsonify({"message": "Settings saved successfully"}), 201

# @settings_bp.route('/settings', methods=['PUT'])
# @jwt_required()
# def update_settings():
#     data = request.get_json()
#     settings = Settings.query.first()
#     if settings:
#         settings.admin_api_key = data['admin_api_key']
#         settings.store_domain = data['store_domain']
#         db.session.commit()
#         return jsonify({"message": "Settings updated successfully"}), 200
#     return jsonify({"message": "Settings not found"}), 404


# --------- 1st one --------------------

from flask import Blueprint, request, jsonify
from models import db, Settings
from flask_jwt_extended import jwt_required
from schemas import SettingsSchema


settings_bp = Blueprint('settings', __name__)
settings_schema = SettingsSchema()
settings_list_schema = SettingsSchema(many=True)

@settings_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    settings = Settings.query.all()
    return jsonify(settings_list_schema.dump(settings)), 200

@settings_bp.route('/settings', methods=['POST'])
@jwt_required()
def create_settings():
    data = request.get_json()
    settings = Settings(admin_api_key=data['admin_api_key'], store_domain=data['store_domain'])
    db.session.add(settings)
    db.session.commit()
    return jsonify({"message": "Settings saved successfully"}), 201

@settings_bp.route('/settings/<int:id>', methods=['PUT'])
@jwt_required()
def update_settings_by_id(id):
    data = request.get_json()
    settings = Settings.query.get(id)
    if settings:
        settings.admin_api_key = data.get('admin_api_key', settings.admin_api_key)
        settings.store_domain = data.get('store_domain', settings.store_domain)
        db.session.commit()
        return jsonify({"message": "Settings updated successfully"}), 200
    else:
        return jsonify({"message": "Settings not found"}), 404