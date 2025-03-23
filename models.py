from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WaitlistEntry(db.Model):
    __tablename__ = 'waitlist_entries'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    use_cases = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, contacted, onboarded
    notes = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'use_cases': self.use_cases.split(','),
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'notes': self.notes,
            'last_updated': self.last_updated.isoformat()
        }

    def __repr__(self):
        return f'<WaitlistEntry {self.email}>' 