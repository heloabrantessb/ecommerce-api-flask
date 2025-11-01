from .auth_controller import auth_bp
from .cart_controller import cart_bp
from .product_controller import product_bp

def register_controller(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)