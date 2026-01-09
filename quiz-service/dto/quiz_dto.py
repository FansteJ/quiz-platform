class QuizCreateDTO:
    """DTO za kreiranje kviza"""
    
    def __init__(self, data):
        self.title = data.get('title')
        self.author_id = data.get('author_id')
        self.author_email = data.get('author_email')
        self.duration = data.get('duration')
        self.questions = data.get('questions', [])
    
    def validate(self):
        """Validacija podataka"""
        errors = []
        
        if not self.title or len(self.title) < 3:
            errors.append('Title must be at least 3 characters')
        
        if not self.author_id:
            errors.append('Author ID is required')
        
        if not self.author_email:
            errors.append('Author email is required')
        
        if not self.duration or self.duration < 10:
            errors.append('Duration must be at least 10 seconds')
        
        if not self.questions or len(self.questions) < 1:
            errors.append('Quiz must have at least 1 question')
        
        # Validacija pitanja
        for idx, question in enumerate(self.questions):
            if not question.get('question_text'):
                errors.append(f'Question {idx + 1}: Question text is required')
            
            if not question.get('points') or question.get('points') < 1:
                errors.append(f'Question {idx + 1}: Points must be at least 1')
            
            answers = question.get('answers', [])
            if len(answers) < 2:
                errors.append(f'Question {idx + 1}: Must have at least 2 answers')
            
            # Provera da li postoji bar jedan tačan odgovor
            correct_count = sum(1 for a in answers if a.get('is_correct'))
            if correct_count < 1:
                errors.append(f'Question {idx + 1}: Must have at least 1 correct answer')
        
        return errors
    
    def to_dict(self):
        """Konvertuje u dictionary za MongoDB"""
        return {
            'title': self.title,
            'author_id': self.author_id,
            'author_email': self.author_email,
            'duration': self.duration,
            'questions': self.questions
        }