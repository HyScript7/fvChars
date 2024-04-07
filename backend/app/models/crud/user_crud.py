from ... import Session
from ..user_model import UserModel


def get_user(db: Session, id) -> UserModel:
    return db.get(UserModel, id)


def get_user_by_email(db: Session, email) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_username(db: Session, username) -> UserModel:
    return db.query(UserModel).filter(UserModel.username == username).first()


def activate_user(db: Session, user: UserModel) -> None:
    if user.active:
        return
    user.active = True
    db.add(user)
    db.commit()


def deactivate_user(db: Session, user: UserModel) -> None:
    if not user.active:
        return
    user.active = False
    db.add(user)
    db.commit()


def create_user(db: Session, username: str, password: str, email: str) -> UserModel:
    user: UserModel = UserModel(username=username, password=password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: UserModel) -> UserModel:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: UserModel) -> None:
    db.delete(user)
    db.commit()
