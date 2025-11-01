from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from src.models import *
from src.database import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    CORS(app)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json

        user = User.query.filter_by(username=data.get("username")).first()
        if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "Logged successfully"})
        return jsonify({"message": "Unauthorized. Invalid username or password"})

    @app.route('/logout', methods=['POST'])
    def logout():
        logout_user()
        return jsonify({"message": "Logout successfully"})

    @app.route('/api/products/add', methods=['POST'])
    @login_required
    def add_product():
        data = request.json
        if 'name' in data and 'price' in data:
            product = Product(name=data['name'], price=data['price'], description=data.get('description', ""))
            db.session.add(product)
            db.session.commit()
            return jsonify({"message": "Product added successfully"}), 200
        return jsonify({"message": "Invalid product data"}), 400

    @app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
    @login_required
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully"}), 200
        return jsonify({"message": "Product not found"}), 404

    @app.route('/api/products/<int:product_id>', methods=['GET'])
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

    @app.route('/api/products/update/<int:product_id>', methods=['PUT'])
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

    @login_manager.user_loader

    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/api/products', methods=['GET'])
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

    # Cart Routes
    @app.route('/api/cart/add/<int:product_id>', methods=['POST'])
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

    @app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
    @login_required
    def remove_from_cart(product_id):
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({"message": "Product removed from the cart successfully"})
        return jsonify({"message": "Failed to remove Product from the cart"})

    @app.route('/api/carts', methods=['GET'])
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

    @app.route('/api/cart/checkout', methods=['POST'])
    @login_required
    def checkout():
        user = User.query.get(int(current_user.id))
        cart_items = user.cart

        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Checkout successfully. Cart has been clear"})


    @app.route('/')
    def index():
        return 'Hello World!'

    return app