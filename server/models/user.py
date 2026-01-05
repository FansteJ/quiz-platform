from models import db
from datetime import datetime

class User(db.Model):
    """
    User model - predstavlja korisnika u bazi
    """
    __tablename__ = 'users'
    
    # Kolone u tabeli
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'M', 'F', 'Ostalo'
    country = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    
    # Uloga korisnika: IGRAC, MODERATOR, ADMINISTRATOR
    role = db.Column(db.String(20), nullable=False, default='PLAYER')
    
    # Slika profila (opciono)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Konvertuje User objekat u dictionary (za JSON)"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'country': self.country,
            'street': self.street,
            'number': self.number,
            'role': self.role,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }