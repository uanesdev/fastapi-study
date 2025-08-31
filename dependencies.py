from models import db
from sqlalchemy.orm import sessionmaker

# Garante que a session é fechada!
def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()