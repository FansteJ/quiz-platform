from flask import Blueprint, request, jsonify
from services.user_service import UserService
from dto.user_dto import RegisterDTO, UserResponseDTO

# Kreiramo Blueprint - to je grupa povezanih ruta
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    POST /api/auth/register
    
    Body (JSON):
    {
        "name": "Marko",
        "surname": "Marković",
        "email": "marko@example.com",
        "password": "securepass123",
        "date_of_birth": "1995-05-15",
        "gender": "M",
        "country": "Serbia",
        "street": "Kralja Petra",
        "number": "10"
    }
    """
    try:
        # Uzmi JSON podatke iz zahteva
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Kreiraj DTO iz podataka
        register_dto = RegisterDTO(data)
        
        # Registruj korisnika kroz servis
        user, error = UserService.register_user(register_dto)
        
        if error:
            return jsonify({
                'success': False,
                'message': 'Registration failed',
                'errors': error.get('errors', [])
            }), 400
        
        # Kreiraj response DTO (bez lozinke!)
        user_response = UserResponseDTO(user)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user_response.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """
    Proverava da li email već postoji
    POST /api/auth/check-email
    Body: { "email": "test@example.com" }
    """
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        exists = UserService.email_exists(email)
        
        return jsonify({
            'success': True,
            'exists': exists
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500