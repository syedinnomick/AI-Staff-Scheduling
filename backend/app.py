from flask import Flask
from flask_cors import CORS
from backend.db.connection import db
from backend.routes.staff_routes import staff_bp
from backend.routes.shift_routes import shift_bp
from backend.routes.schedule_routes import schedule_bp
import os

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for all routes
    db_url = os.getenv("DATABASE_URL", "sqlite:///scheduling.db")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # register routes
    app.register_blueprint(staff_bp, url_prefix="/api")
    app.register_blueprint(shift_bp, url_prefix="/api")
    app.register_blueprint(schedule_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)