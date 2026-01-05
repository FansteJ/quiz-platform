from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from models.user import User
from config import Config

# Import Blueprint-a
from routes.auth_routes import auth_bp

# Kreiramo Flask aplikaciju
app = Flask(__name__)

# Učitavamo konfiguraciju
app.config.from_object(Config)

# Omogući CORS za komunikaciju sa React-om
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Inicijalizujemo bazu podataka
db.init_app(app)

# Registrujemo Blueprint-ove
app.register_blueprint(auth_bp)

# Kreiramo tabele u bazi
with app.app_context():
    db.create_all()
    print("✅ Database created!")

@app.route('/')
def hello():
    return jsonify({
        'message': 'Quiz Platform API is running!',
        'status': 'success',
        'database': 'connected'
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