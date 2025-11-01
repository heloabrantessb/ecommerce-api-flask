from flask import Blueprint, jsonify, request
from flask_login import login_required

from src.models import Product
from src.database import db

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

@product_bp.route('/add', methods=['POST'])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'], description=data.get('description', ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 200
    return jsonify({"message": "Invalid product data"}), 400


@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Product not found"}), 404


@product_bp.route('/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
        product_list.append(product_data)
    return jsonify(product_list), 200