from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        assert name is not None, 'Author must have a name'
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        assert phone_number is not None and len(phone_number) == 10, 'Phone number must be exactly 10 digits.'
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        assert title is not None, 'Post must have a title.'
        assert self.is_clickbait(title), 'Title must be clickbait'
        return title
    
    @staticmethod
    def is_clickbait(title):
        patterns = [
            "Won't Believe",
            "Secret",
            r"Top \d+",
            "Guess"
        ]
        for pattern in patterns:
            if re.search(pattern, title, re.IGNORECASE):
                return True
        return False
    
    @validates('content')
    def validate_content(self, key, content):
        assert content is not None and len(content) >= 250, 'Post content must be at least 250 characters.'
        return content
    
    @validates('summary')
    def validates_summary(self, key, summary):
        assert summary is not None and len(summary) < 250, ' Post summary must be a maximum of 250 characters.'
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        assert category in ['Fiction', 'Non-Fiction'], "Post category must be either 'Fiction' or 'Non-Fiction'."
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
