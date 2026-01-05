from datetime import datetime, timedelta
from models import db
from models.user import User
from models.login_attempt import LoginAttempt
from services.user_service import UserService

class AuthService:
    """Servis za autentifikaciju"""
    
    BLOCK_DURATION_MINUTES = 15  # Blokada traje 15 minuta
    MAX_FAILED_ATTEMPTS = 3  # Maksimalno 3 neuspešna pokušaja
    
    @staticmethod
    def record_login_attempt(email: str, success: bool, ip_address: str = None):
        """Beleži pokušaj prijave"""
        attempt = LoginAttempt(
            email=email.lower(),
            success=success,
            ip_address=ip_address,
            attempted_at=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
    
    @staticmethod
    def get_failed_attempts_count(email: str) -> int:
        """Broji neuspešne pokušaje u poslednjih 15 minuta"""
        time_threshold = datetime.utcnow() - timedelta(minutes=AuthService.BLOCK_DURATION_MINUTES)
        
        failed_count = LoginAttempt.query.filter(
            LoginAttempt.email == email.lower(),
            LoginAttempt.success == False,
            LoginAttempt.attempted_at >= time_threshold
        ).count()
        
        return failed_count
    
    @staticmethod
    def is_user_blocked(email: str) -> tuple:
        """
        Proverava da li je korisnik blokiran
        Returns: (is_blocked: bool, remaining_time: int)
        """
        time_threshold = datetime.utcnow() - timedelta(minutes=AuthService.BLOCK_DURATION_MINUTES)
        
        # Pronađi poslednji neuspešan pokušaj
        last_failed = LoginAttempt.query.filter(
            LoginAttempt.email == email.lower(),
            LoginAttempt.success == False,
            LoginAttempt.attempted_at >= time_threshold
        ).order_by(LoginAttempt.attempted_at.desc()).first()
        
        if not last_failed:
            return False, 0
        
        # Broji neuspešne pokušaje
        failed_count = AuthService.get_failed_attempts_count(email)
        
        if failed_count >= AuthService.MAX_FAILED_ATTEMPTS:
            # Izračunaj preostalo vreme blokade
            time_since_last = datetime.utcnow() - last_failed.attempted_at
            remaining_minutes = AuthService.BLOCK_DURATION_MINUTES - int(time_since_last.total_seconds() / 60)
            
            if remaining_minutes > 0:
                return True, remaining_minutes
        
        return False, 0
    
    @staticmethod
    def clear_failed_attempts(email: str):
        """Briše neuspešne pokušaje nakon uspešne prijave"""
        # Možemo ostaviti u bazi za statistiku, samo zapisujemo uspešan pokušaj
        AuthService.record_login_attempt(email, success=True)
    
    @staticmethod
    def authenticate_user(email: str, password: str):
        """
        Autentifikuje korisnika
        Returns: (user, error)
        """
        email = email.lower()
        
        # 1. Proveri da li je korisnik blokiran
        is_blocked, remaining_time = AuthService.is_user_blocked(email)
        
        if is_blocked:
            return None, {
                'message': f'Too many failed attempts. Account is locked for {remaining_time} more minutes.',
                'blocked': True,
                'remaining_time': remaining_time
            }
        
        # 2. Pronađi korisnika
        user = UserService.get_user_by_email(email)
        
        if not user:
            # Beleži neuspešan pokušaj
            AuthService.record_login_attempt(email, success=False)
            
            # Proveri da li je sada blokiran
            failed_count = AuthService.get_failed_attempts_count(email)
            remaining_attempts = AuthService.MAX_FAILED_ATTEMPTS - failed_count
            
            return None, {
                'message': 'Invalid email or password',
                'remaining_attempts': remaining_attempts if remaining_attempts > 0 else 0
            }
        
        # 3. Proveri lozinku
        if not UserService.verify_password(password, user.password_hash):
            # Beleži neuspešan pokušaj
            AuthService.record_login_attempt(email, success=False)
            
            # Proveri da li je sada blokiran
            failed_count = AuthService.get_failed_attempts_count(email)
            remaining_attempts = AuthService.MAX_FAILED_ATTEMPTS - failed_count
            
            if remaining_attempts <= 0:
                return None, {
                    'message': f'Too many failed attempts. Account is locked for {AuthService.BLOCK_DURATION_MINUTES} minutes.',
                    'blocked': True,
                    'remaining_time': AuthService.BLOCK_DURATION_MINUTES
                }
            
            return None, {
                'message': 'Invalid email or password',
                'remaining_attempts': remaining_attempts
            }
        
        # 4. Uspešna prijava - obriši neuspešne pokušaje
        AuthService.clear_failed_attempts(email)
        
        return user, None