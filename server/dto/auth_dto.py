class LoginDTO:
    """DTO za login zahtev"""
    
    def __init__(self, data):
        self.email = data.get('email')
        self.password = data.get('password')
    
    def validate(self):
        """Validacija login podataka"""
        errors = []
        
        if not self.email or '@' not in self.email:
            errors.append('Invalid email address')
        
        if not self.password:
            errors.append('Password is required')
        
        return errors


class LoginResponseDTO:
    """DTO za login odgovor"""
    
    def __init__(self, access_token, refresh_token, user):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'role': user.role,
            'profile_image': user.profile_image
        }
    
    def to_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'user': self.user
        }