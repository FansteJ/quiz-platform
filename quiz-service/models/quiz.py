from datetime import datetime
from bson import ObjectId
from database import Database

class Quiz:
    """
    Quiz model za MongoDB
    
    Struktura:
    {
        "_id": ObjectId,
        "title": "Naziv kviza",
        "author_id": 123,  # User ID iz PostgreSQL
        "author_email": "moderator@example.com",
        "duration": 300,  # sekunde
        "status": "pending",  # pending, approved, rejected
        "rejection_reason": null,
        "questions": [
            {
                "question_text": "Pitanje?",
                "points": 10,
                "answers": [
                    {"text": "Odgovor 1", "is_correct": true},
                    {"text": "Odgovor 2", "is_correct": false}
                ]
            }
        ],
        "created_at": datetime,
        "updated_at": datetime
    }
    """
    
    COLLECTION = 'quizzes'
    
    @staticmethod
    def get_collection():
        """Vraća quizzes kolekciju"""
        db = Database.get_db()
        return db[Quiz.COLLECTION]
    
    @staticmethod
    def create(quiz_data):
        """
        Kreira novi kviz
        Returns: inserted_id
        """
        collection = Quiz.get_collection()
        
        quiz_data['status'] = 'pending'  # Svi novi kvizovi čekaju odobrenje
        quiz_data['rejection_reason'] = None
        quiz_data['created_at'] = datetime.utcnow()
        quiz_data['updated_at'] = datetime.utcnow()
        
        result = collection.insert_one(quiz_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(quiz_id):
        """Pronalazi kviz po ID-u"""
        collection = Quiz.get_collection()
        return collection.find_one({'_id': ObjectId(quiz_id)})
    
    @staticmethod
    def find_all(status=None, author_id=None):
        """
        Pronalazi sve kvizove sa opcionalnim filterima
        """
        collection = Quiz.get_collection()
        query = {}
        
        if status:
            query['status'] = status
        
        if author_id:
            query['author_id'] = author_id
        
        return list(collection.find(query).sort('created_at', -1))
    
    @staticmethod
    def update(quiz_id, update_data):
        """Ažurira kviz"""
        collection = Quiz.get_collection()
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {'_id': ObjectId(quiz_id)},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(quiz_id):
        """Briše kviz"""
        collection = Quiz.get_collection()
        result = collection.delete_one({'_id': ObjectId(quiz_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def approve(quiz_id):
        """Odobrava kviz (administrator)"""
        return Quiz.update(quiz_id, {'status': 'approved', 'rejection_reason': None})
    
    @staticmethod
    def reject(quiz_id, reason):
        """Odbija kviz (administrator)"""
        return Quiz.update(quiz_id, {'status': 'rejected', 'rejection_reason': reason})
    
    @staticmethod
    def to_dict(quiz):
        """Konvertuje MongoDB dokument u Python dict"""
        if not quiz:
            return None
        
        quiz['id'] = str(quiz['_id'])
        del quiz['_id']
        
        # Konvertuj datetime u ISO string
        if 'created_at' in quiz:
            quiz['created_at'] = quiz['created_at'].isoformat()
        if 'updated_at' in quiz:
            quiz['updated_at'] = quiz['updated_at'].isoformat()
        
        return quiz