from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import os
import psycopg2

db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://yjwipptkfagjrk:60849b67bf32dba8da4f4e45ac0bc174b04627508f425e21d83048a727e5d6f5@ec2-34-236-199-229.compute-1.amazonaws.com:5432/d1b7i31omjl47r')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    with app.app_context():
        # 創建數據庫表格（如果不存在）
        db.create_all()

    return app