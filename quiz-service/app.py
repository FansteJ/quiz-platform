from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import Database
from routes.quiz_routes import quiz_bp

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

# Register blueprints
app.register_blueprint(quiz_bp)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Quiz Service API is running!',
        'service': 'quiz-service',
        'status': 'success'
    })

@app.route('/health')
def health():
    try:
        # Proveri MongoDB konekciju
        db = Database.get_db()
        db.command('ping')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)