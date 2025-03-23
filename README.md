![image](https://github.com/user-attachments/assets/f8123c11-5861-441e-8814-71011d328193)
![image](https://github.com/user-attachments/assets/d8a3328b-f6b8-4e1e-8543-ac73618b70c3)



# Gnosi Waitlist

A modern waitlist management system for Gnosi social media agentic content creation platform that handles user registration and notifications.

## Description

Gnosi Waitlist is a Flask-based application that manages the pre-launch registration process for the Gnosi platform. It handles user signups, email verifications, and automated notifications for product launches and updates.

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy
- PostgreSQL
- Redis (for queue management)
- Celery (for background tasks)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tilakcsp/gnosi
cd gnosi
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. Initialize the database:
```bash
flask db upgrade
```

## Usage

1. Start the development server:
```bash
flask run
```

2. Start Celery worker (in a separate terminal):
```bash
celery -A app.celery worker --loglevel=info
```

3. Access the application at `http://localhost:5000`

### API Endpoints

- `POST /api/register` - Register new user
- `GET /api/status` - Check waitlist position
- `POST /api/verify` - Verify email address

## Features

- Secure user registration and data storage
- Email verification system
- Automated position tracking in waitlist
- Admin dashboard for waitlist management
- RESTful API endpoints
- Rate limiting and spam protection
- Background task processing
- Email notifications for:
  - Registration confirmation
  - Position updates
  - Launch announcements



## Contact

Project Maintainer - Tilak
Project Link: https://github.com/tilakcsp/gnosi

