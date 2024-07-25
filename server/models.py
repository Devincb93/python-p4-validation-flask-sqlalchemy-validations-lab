from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if len(name) <= 0:
            raise ValueError("Please enter a valid new Author")
        if db.session.query(Author).filter(Author.name == name).first():
            raise ValueError("Name already exists in database")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits")
        if not phone_number.isdigit():
            raise ValueError("Phone number must only be digits")
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

    @validates('content') 
    def validates_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Not enough characters please add more")
        return content
        

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Maximum amount of characters(250) reached")
        return summary

    @validates('title')
    def validate_title(self, key, title):
        clickbait_titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_titles):
            raise ValueError("Title must contain an approved title beginner")
        return title
    
    @validates('category')
    def validate_category(self, key, category):
        categories = ["Fiction", "Non-Fiction"]
        if not any(type in category for type in categories):
            raise ValueError("Category must be one from the approved list")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
