from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import re

from database import get_db, EmailSubscription

app = FastAPI(title="OpenSlot.ai Email Collection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://lp-frontend-calendar-6zaj.vercel.app"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email: str

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.get("/")
async def root():
    return {"message": "OpenSlot.ai Email API is running!", "status": "success"}

@app.post("/api/subscribe")
async def save_email(request: EmailRequest, db: Session = Depends(get_db)):
    # Validate email
    if not is_valid_email(request.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Normalize email
    email = request.email.lower().strip()
    
    try:
        # Check if email already exists
        existing = db.query(EmailSubscription).filter(EmailSubscription.email == email).first()
        if existing:
            return {"message": "Email already registered!", "success": True}
        
        # Save new email
        subscription = EmailSubscription(email=email)
        db.add(subscription)
        db.commit()
        
        return {"message": "Email saved successfully!", "success": True}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save email")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)