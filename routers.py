from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import time

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_timestamp = int(expiration.replace(tzinfo=timezone.utc).timestamp())

    return {"access_token": access_token,
            "token_type": "bearer",
            "role": user.role,
            "exp": expiration_timestamp}


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.post("/users/update_role/", response_model=schemas.User)
def update_user_role(user: schemas.UserUpdate, db: Session = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    if not crud.user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to update user roles")
    user = crud.update_user_role(db=db, user_id=user.id, new_role=user.role)
    if not user:
        raise HTTPException(status_code=404, detail="Role not found")
    return user


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to delete users")
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="Cannot delete yourself")
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id)


@router.post("/create_event/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):
    if not crud.user_is_organizer(current_user) and not crud.user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to create events")
    return crud.create_event(db=db, event=event, user_id=current_user.id)


@router.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.delete("/events/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    event = crud.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != current_user.id and not crud.user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")

    tickets = crud.get_tickets_by_event_id(db, event_id=event_id)  # Assuming this function exists
    for ticket in tickets:
        crud.delete_ticket(db, ticket_id=ticket.id)  # Assuming this function exists

    return crud.delete_event(db, event_id)


@router.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.post("/events/{event_id}/comments/", response_model=schemas.Comment)
def create_comment_for_event(event_id: int, comment: schemas.CommentCreate,
                             db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id, event_id=event_id)


@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    comment = crud.get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and not crud.user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    return crud.delete_comment(db, comment_id)


@router.get("/comments/{event_id}", response_model=List[schemas.Comment])
def read_comments(event_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, event_id=event_id)
    return comments


@router.get("/tickets/{event_id}", response_model=schemas.HasTicket)
def has_ticket(event_id: int, db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    if crud.has_ticket(db=db, user_id=current_user.id, event_id=event_id):
        return {"has_ticket": True}
    else:
        return {"has_ticket": False}


@router.post("/tickets/{event_id}", response_model=schemas.Ticket)
def create_ticket(event_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(get_current_user)):
    if has_ticket(event_id=event_id, db=db, current_user=current_user)['has_ticket']:
        raise HTTPException(status_code=403, detail="Already has ticket")
    return crud.create_ticket(db=db, user_id=current_user.id, event_id=event_id)



