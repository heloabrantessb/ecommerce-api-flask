from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from src.models import User, Product, CartItem
from src.database import db

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(int(product_id))

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Product added to the cart successfully"}), 200
    return jsonify({"message": "Failed to add Product to the cart"}), 400


@cart_bp.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Product removed from the cart successfully"})
    return jsonify({"message": "Failed to remove Product from the cart"})

@cart_bp.route('/api/carts', methods=['GET'])
def view_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_list = []
    for cart_item in cart_items:
        product = Product.get
        cart_list.append({
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "product_info": {
                "name": product.name,
                "price": product.price,
                "description": product.description
            }
        })
    return jsonify(cart_list), 200


@cart_bp.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart

    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Checkout successfully. Cart has been clear"})

