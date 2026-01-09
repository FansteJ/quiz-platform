from flask import Blueprint, request, jsonify
from models.quiz import Quiz
from dto.quiz_dto import QuizCreateDTO

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

@quiz_bp.route('/create', methods=['POST'])
def create_quiz():
    """
    Kreira novi kviz (MODERATOR)
    
    POST /api/quiz/create
    Body: {
        "title": "Naziv kviza",
        "author_id": 123,
        "author_email": "moderator@example.com",
        "duration": 300,
        "questions": [...]
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
        quiz_dto = QuizCreateDTO(data)
        errors = quiz_dto.validate()
        
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Kreiraj kviz
        quiz_id = Quiz.create(quiz_dto.to_dict())
        
        # Učitaj kreirani kviz
        created_quiz = Quiz.find_by_id(quiz_id)
        
        return jsonify({
            'success': True,
            'message': 'Quiz created successfully. Waiting for admin approval.',
            'quiz': Quiz.to_dict(created_quiz)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


@quiz_bp.route('/list', methods=['GET'])
def list_quizzes():
    """
    Lista kvizova
    
    Query params:
    - status: pending, approved, rejected
    - author_id: filtriraj po autoru
    """
    try:
        status = request.args.get('status')
        author_id = request.args.get('author_id')
        
        if author_id:
            author_id = int(author_id)
        
        quizzes = Quiz.find_all(status=status, author_id=author_id)
        
        return jsonify({
            'success': True,
            'count': len(quizzes),
            'quizzes': [Quiz.to_dict(q) for q in quizzes]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quiz_bp.route('/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Vraća pojedinačni kviz"""
    try:
        quiz = Quiz.find_by_id(quiz_id)
        
        if not quiz:
            return jsonify({
                'success': False,
                'message': 'Quiz not found'
            }), 404
        
        return jsonify({
            'success': True,
            'quiz': Quiz.to_dict(quiz)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quiz_bp.route('/<quiz_id>/approve', methods=['POST'])
def approve_quiz(quiz_id):
    """Odobrava kviz (ADMINISTRATOR)"""
    try:
        success = Quiz.approve(quiz_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Quiz not found or already approved'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Quiz approved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quiz_bp.route('/<quiz_id>/reject', methods=['POST'])
def reject_quiz(quiz_id):
    """Odbija kviz (ADMINISTRATOR)"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'No reason provided')
        
        success = Quiz.reject(quiz_id, reason)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Quiz not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Quiz rejected'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@quiz_bp.route('/<quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Briše kviz (MODERATOR ili ADMINISTRATOR)"""
    try:
        success = Quiz.delete(quiz_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Quiz not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Quiz deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500