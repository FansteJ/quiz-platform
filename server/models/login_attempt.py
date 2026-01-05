from models import db
from datetime import datetime

class LoginAttempt(db.Model):
    """
    Model za praćenje neuspešnih pokušaja prijave
    Koristi se za blokadu korisnika nakon 3 neuspešna pokušaja
    """
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    success = db.Column(db.Boolean, nullable=False, default=False)
    ip_address = db.Column(db.String(50), nullable=True)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<LoginAttempt {self.email} - {"Success" if self.success else "Failed"}>'