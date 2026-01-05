import bcrypt
from datetime import datetime
from models import db
from models.user import User
from dto.user_dto import RegisterDTO, UserResponseDTO

class UserService:
    """Servis za upravljanje korisnicima"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hešuje lozinku koristeći bcrypt"""
        # Generišemo salt i hešujemo lozinku
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Proverava da li se lozinka poklapa sa hešom"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    @staticmethod
    def email_exists(email: str) -> bool:
        """Proverava da li email već postoji u bazi"""
        return User.query.filter_by(email=email).first() is not None
    
    @staticmethod
    def register_user(register_dto: RegisterDTO):
        """
        Registruje novog korisnika
        Returns: (user, error)
        """
        # Validacija
        errors = register_dto.validate()
        if errors:
            return None, {'errors': errors}
        
        # Proveri da li email već postoji
        if UserService.email_exists(register_dto.email):
            return None, {'errors': ['Email already exists']}
        
        try:
            # Konvertuj datum iz string-a u date objekat
            date_of_birth = datetime.strptime(
                register_dto.date_of_birth, 
                '%Y-%m-%d'
            ).date()
            
            # Hešuj lozinku
            password_hash = UserService.hash_password(register_dto.password)
            
            # Kreiraj novog korisnika
            new_user = User(
                name=register_dto.name,
                surname=register_dto.surname,
                email=register_dto.email.lower(),  # Email u lowercase
                password_hash=password_hash,
                date_of_birth=date_of_birth,
                gender=register_dto.gender,
                country=register_dto.country,
                street=register_dto.street,
                number=register_dto.number,
                role='PLAYER'  # Svi novi korisnici su igrači
            )
            
            # Sačuvaj u bazu
            db.session.add(new_user)
            db.session.commit()
            
            return new_user, None
            
        except ValueError as e:
            return None, {'errors': ['Invalid date format. Use YYYY-MM-DD']}
        except Exception as e:
            db.session.rollback()
            return None, {'errors': [f'Registration failed: {str(e)}']}
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Pronalazi korisnika po ID-u"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email: str):
        """Pronalazi korisnika po email-u"""
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def get_all_users():
        """Vraća sve korisnike (za administratora)"""
        return User.query.all()