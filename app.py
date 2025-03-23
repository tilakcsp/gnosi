from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from models import db, WaitlistEntry

app = Flask(__name__, static_folder='.')
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/waitlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

# Initialize database
db.init_app(app)

# Create database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        email = data.get('email')
        use_cases = ','.join(data.get('useCases', []))

        if not email or not use_cases:
            return jsonify({'error': 'Email and use cases are required'}), 400

        # Check if email already exists
        existing_entry = WaitlistEntry.query.filter_by(email=email).first()
        if existing_entry:
            return jsonify({'error': 'Email already registered'}), 400

        # Create new entry
        new_entry = WaitlistEntry(
            email=email,
            use_cases=use_cases,
            status='pending'
        )

        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            'message': 'Successfully joined the waitlist!',
            'entry': new_entry.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries', methods=['GET'])
def get_entries():
    try:
        status = request.args.get('status')
        query = WaitlistEntry.query
        
        if status:
            query = query.filter_by(status=status)
            
        entries = query.order_by(WaitlistEntry.created_at.desc()).all()
        return jsonify([entry.to_dict() for entry in entries]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    try:
        entry = WaitlistEntry.query.get_or_404(entry_id)
        data = request.get_json()
        
        if 'status' in data:
            entry.status = data['status']
        if 'notes' in data:
            entry.notes = data['notes']
            
        db.session.commit()
        return jsonify(entry.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 