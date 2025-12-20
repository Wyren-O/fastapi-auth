from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.services import auth
from app.schemas import schemas
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_user_from_token(token, db)
    if not user:
        raise HTTPException(
            status_code=401
        )
    return user

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created_user = auth.register_user(user, db)
    if not created_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    return created_user
    
@router.post("/login")
def login_user_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(auth.models.User).filter(auth.models.User.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )
        
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user
