from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()