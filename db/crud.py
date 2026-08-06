from sqlmodel import Session,select

from .models import Token

def create_token(
    session: Session,
    data: Token,
):
    session.add(data)

    session.commit()

    session.refresh(data)

    return data
def get_token(
    session: Session,
    token_id: str,
):

    statement = select(Token).where(
        Token.token_id == token_id
    )

    return session.exec(statement).first()