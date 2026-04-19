import os
from flask import Flask
from config import Config
from extensions import mysql
from routes.public import public_bp
from routes.auth import auth_bp
from routes.portal import portal_bp, current_user
from models import ensure_portal_tables


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    mysql.init_app(app)

    with app.app_context():
        ensure_portal_tables()

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(portal_bp)

    @app.context_processor
    def inject_current_year():
        return {'current_year': __import__('datetime').datetime.now().year}

    @app.context_processor
    def inject_current_user():
        return {'current_user': current_user()}

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
