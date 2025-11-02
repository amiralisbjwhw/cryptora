from sqlmodel import create_engine, SQLModel
from models import User, OTPUser, Message, Group, GroupMember, GroupMessage

engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
