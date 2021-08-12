from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()



class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable = False, unique = True, primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    feedbacks = db.relationship("Feedback",backref="user",cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, firstname, lastname, email):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username = username,
            password = hashed_utf8,
            email = email,
            firstname = firstname,
            lastname = lastname
        )

        db.session.add(user)
        return user

    @classmethod
    def login(cls, username, password):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):

    __tablename__ = 'feedback'
    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True)
    title = db.Column(
        db.String(100),
        nullable=False)
    content = db.Column(
        db.String(),
        nullable=False)
    username = db.Column(
        db.ForeignKey('users.username'),
        nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)