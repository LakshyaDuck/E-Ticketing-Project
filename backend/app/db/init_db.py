from app.db.base import Base
from app.db.session import engine

# Import models so metadata is registered
from app.models import User  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)
