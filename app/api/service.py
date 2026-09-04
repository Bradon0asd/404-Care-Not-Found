from sqlalchemy.exc import IntegrityError

from app.common.errors import UserAlreadyExistsError, UserNotFoundError
from app.extensions import db
from app.models import User


def create_user(*, line_user_id, name=None):
    user = User(line_user_id=line_user_id, name=name)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise UserAlreadyExistsError("User already exists") from error
    return user


def get_user(*, user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise UserNotFoundError("User not found")
    return user


def get_or_create_user(*, line_user_id, name=None):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    if user is not None:
        return user
    return create_user(line_user_id=line_user_id, name=name)
