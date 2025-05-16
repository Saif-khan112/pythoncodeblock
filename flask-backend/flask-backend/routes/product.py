from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product
from schemas import ProductSchema
from services import get_shopify_products

product_bp = Blueprint('product', __name__)
product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)

# Get all products
@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    # products = get_shopify_products()
    products = Product.query.limit(4).all()
    product_schema = ProductSchema(many=True)
    serialized_products = product_schema.dump(products)
    return jsonify(serialized_products), 200

