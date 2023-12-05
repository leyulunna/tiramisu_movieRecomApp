from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    with app.app_context():
        # 創建數據庫表格（如果不存在）
        db.create_all()

    return app
