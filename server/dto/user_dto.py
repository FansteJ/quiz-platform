from datetime import date

class RegisterDTO:
    """DTO za registraciju korisnika"""
    
    def __init__(self, data):
        self.name = data.get('name')
        self.surname = data.get('surname')
        self.email = data.get('email')
        self.password = data.get('password')
        self.date_of_birth = data.get('date_of_birth')
        self.gender = data.get('gender')
        self.country = data.get('country')
        self.street = data.get('street')
        self.number = data.get('number')
    
    def validate(self):
        """Validacija podataka"""
        errors = []
        
        if not self.name or len(self.name) < 2:
            errors.append('Name must be at least 2 characters')
        
        if not self.surname or len(self.surname) < 2:
            errors.append('Surname must be at least 2 characters')
        
        if not self.email or '@' not in self.email:
            errors.append('Invalid email address')
        
        if not self.password or len(self.password) < 6:
            errors.append('Password must be at least 6 characters')
        
        if not self.date_of_birth:
            errors.append('Date of birth is required')
        
        if self.gender not in ['M', 'F', 'Other']:
            errors.append('Gender must be M, F, or Other')
        
        if not self.country:
            errors.append('Country is required')
        
        if not self.street:
            errors.append('Street is required')
        
        if not self.number:
            errors.append('Number is required')
        
        return errors
    
    def to_dict(self):
        """Konvertuje DTO u dictionary"""
        return {
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'country': self.country,
            'street': self.street,
            'number': self.number
        }


class UserResponseDTO:
    """DTO za vraćanje korisničkih podataka (bez lozinke!)"""
    
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.surname = user.surname
        self.email = user.email
        self.date_of_birth = user.date_of_birth.isoformat() if user.date_of_birth else None
        self.gender = user.gender
        self.country = user.country
        self.street = user.street
        self.number = user.number
        self.role = user.role
        self.profile_image = user.profile_image
        self.created_at = user.created_at.isoformat() if user.created_at else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'country': self.country,
            'street': self.street,
            'number': self.number,
            'role': self.role,
            'profile_image': self.profile_image,
            'created_at': self.created_at
        }