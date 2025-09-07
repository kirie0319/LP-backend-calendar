# OpenSlot.ai Backend

Simple FastAPI backend for collecting email subscriptions from the landing page.

## Setup

1. Create virtual environment: `python3 -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Make sure `.env` file has your PostgreSQL database URL
5. Start the server: `./start.sh` or `python main.py`

## API Endpoints

### POST `/api/subscribe`
Save user email to database.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Email saved successfully!",
  "success": true
}
```

## Database
- Uses PostgreSQL with SQLAlchemy ORM
- Automatically creates `email_subscriptions` table
- Stores: id, email, created_at

## Features
- ✅ Email validation
- ✅ Duplicate email handling
- ✅ CORS enabled for frontend
- ✅ PostgreSQL database connection
- ✅ Automatic table creation
