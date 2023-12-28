from sqlalchemy.orm import Session
import models
import schemas

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    # Создание экземпляра модели Event, заполненного данными из event (объекта EventCreate).
    db_event = models.Event(**event.model_dump(), user_id=user_id)
    # Добавление объекта в сессию базы данных.
    db.add(db_event)
    # Фиксация (commit) транзакции, чтобы сохранить объект в базе данных.
    db.commit()
    # Обновление экземпляра объекта данными из базы данных (например, получение ID).
    db.refresh(db_event)
    # Возврат созданного события.
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return db_event


def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, event_id: int):
    db_comment = models.Comment(**comment.model_dump(), user_id=user_id, event_id=event_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return db_comment


def get_comments(db: Session, event_id: int):
    return db.query(models.Comment).filter(models.Comment.event_id == event_id).all()


def create_ticket(db: Session, user_id: int, event_id: int):
    db_ticket = models.Ticket(user_id=user_id, event_id=event_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def has_ticket(db: Session, user_id: int, event_id: int):
    return db.query(models.Ticket).filter(models.Ticket.user_id == user_id, models.Ticket.event_id == event_id).first()


def get_tickets_by_event_id(db: Session, event_id: int):
    return db.query(models.Ticket).filter(models.Ticket.event_id == event_id).all()


def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
        return db_ticket


def update_user_role(db: Session, user_id: int, new_role: str):
    if new_role not in ['user', 'organizer', 'admin']:
        return None
    db_user = get_user(db, user_id)
    if db_user:
        db_user.role = new_role
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


def user_is_organizer(user: models.User):
    return user.role == 'organizer'


def user_is_admin(user: models.User):
    return user.role == 'admin'
