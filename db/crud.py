from sqlmodel import Session, select, update
from .models import Token
from models.models import TokenColumn


def create_token(
    session: Session,
    token: Token,
) -> Token:
    session.add(token)
    session.commit()
    session.refresh(token)
    return token


def get_token(
    session: Session,
    token_id: str,
) -> Token | None:
    statement = select(Token).where(Token.token_id == token_id)
    return session.exec(statement).first()


def update_token(
    session: Session,
    token_id: str,
    column: TokenColumn,
    value,
) -> Token | None:
    token = get_token(session, token_id)

    if token is None:
        return None

    setattr(token, column.value, value)

    session.commit()
    session.refresh(token)

    return token
