from flask import Flask, jsonify
from models import db
from models.user import User
from config import Config

# Kreiramo Flask aplikaciju
app = Flask(__name__)

# Učitavamo konfiguraciju
app.config.from_object(Config)

# Inicijalizujemo bazu podataka
db.init_app(app)

# Kreiramo tabele u bazi
with app.app_context():
    db.create_all()
    print("✅ Baza podataka kreirana!")

@app.route('/')
def hello():
    return jsonify({
        'message': 'Quiz Platform API radi!',
        'status': 'success',
        'database': 'connected'
    })

@app.route('/health')
def health():
    # Proveri da li baza radi
    try:
        # Jednostavan upit ka bazi
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status
    })

@app.route('/test-user')
def test_user():
    """Endpoint za testiranje kreiranja korisnika"""
    try:
        # Proveri da li korisnik već postoji
        existing_user = User.query.filter_by(email='test@example.com').first()
        
        if existing_user:
            return jsonify({
                'message': 'Korisnik već postoji',
                'user': existing_user.to_dict()
            })
        
        # Kreiraj test korisnika
        from datetime import date
        test_user = User(
            name='Marko',
            surname='Marković',
            email='test@example.com',
            password_hash='hash123',  # Later ćemo dodati pravo hešovanje
            date_of_birth=date(1995, 5, 15),
            gender='M',
            country='Srbija',
            street='Kralja Petra',
            number='10',
            role='PLAYER'
        )
        
        # Dodaj u bazu
        db.session.add(test_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Korisnik uspešno kreiran!',
            'user': test_user.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)