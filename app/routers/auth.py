from fastapi import APIRouter,Depends,HTTPException
from app.services import auth
from app.schemas import schemas
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/register")

@router.post("")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created_user = auth.register_user(user, db)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created_user
    

