from flask import Flask
from model import db, login_manager
from routes import bp as routes_bp
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_DATABASE_URI'] =   "postgresql://default:HQrEt0nuO3wp@ep-jolly-snow-a5smrx8g.us-east-2.aws.neon.tech:5432/verceldb?sslmode=require"

    app.config['SECRET_KEY'] = 'secret-key'
    
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
