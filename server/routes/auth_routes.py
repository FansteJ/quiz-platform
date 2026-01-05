from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from services.user_service import UserService
from services.auth_service import AuthService
from dto.user_dto import RegisterDTO, UserResponseDTO
from dto.auth_dto import LoginDTO, LoginResponseDTO

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registracija novog korisnika"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        register_dto = RegisterDTO(data)
        user, error = UserService.register_user(register_dto)
        
        if error:
            return jsonify({
                'success': False,
                'message': 'Registration failed',
                'errors': error.get('errors', [])
            }), 400
        
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


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login korisnika
    
    POST /api/auth/login
    Body: {
        "email": "petar@example.com",
        "password": "securepass123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validacija
        login_dto = LoginDTO(data)
        errors = login_dto.validate()
        
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Autentifikacija
        user, error = AuthService.authenticate_user(
            login_dto.email,
            login_dto.password
        )
        
        if error:
            status_code = 423 if error.get('blocked') else 401
            return jsonify({
                'success': False,
                **error
            }), status_code
        
        # Generiši JWT tokene
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Response
        login_response = LoginResponseDTO(access_token, refresh_token, user)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            **login_response.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    Header: Authorization: Bearer <refresh_token>
    """
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Vraća podatke trenutno ulogovanog korisnika
    Header: Authorization: Bearer <access_token>
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = UserService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user_response = UserResponseDTO(user)
        
        return jsonify({
            'success': True,
            'user': user_response.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout korisnika (frontend briše token)
    """
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200