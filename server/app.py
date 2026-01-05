from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# JWT
jwt = JWTManager(app)

# Database
db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp)

# Kreiraj tabele
with app.app_context():
    db.create_all()
    print("✅ Database created!")

@app.route('/')
def hello():
    return jsonify({
        'message': 'Quiz Platform API is running!',
        'status': 'success'
    })

@app.route('/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)