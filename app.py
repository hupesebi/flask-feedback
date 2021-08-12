from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)


@app.route('/')
def home():
    return redirect ('/register')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data

        user = User.register(username, password, firstname, lastname, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'username in session':
        return redirect (f"/users/{session['username']}")
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username or password']
            return render_template('login.html')

@app.route('/users/<username>')
def show_user_info(username):
    if "username" not in session:
        flash("Please login first!")
        return redirect('/login')
    elif session["username"] != username:
        flash("You are not authorized to view that page!")
        return redirect(f'/users/{session["username"]}')
    user = User.query.get_or_404(username)
    return render_template('user_info.html', user=user)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Hope to see you soon again!")
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def handle_feedback(username):
    """Shows feedback form and handles data submission for same."""
    if "username" not in session:
        flash("Please login first!")
        return redirect('/login')
    User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback submitted!', "success")
        return redirect(f'/users/{username}')
    else:
        return render_template('add_feedback.html', form=form)

@app.route('/users/<username>/delete')
def delete_user(username):
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    flash(f"Account for {username} deleted.", "danger")
    return redirect('/login')
    