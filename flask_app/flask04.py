
# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask 
from flask import render_template
from flask import request  # Flask is the web app that we will customize
from flask import redirect, url_for
from database import db
from models import Note as Note
from models import User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    a_user = db.session.query(User).filter_by(email='dshelt10@uncc.edu').one()

    return render_template('index.html', user = a_user)


@app.route('/notes')
def get_notes():
    a_user = db.session.query(User).filter_by(email='dshelt10@uncc.edu').one()

    my_notes = db.session.query(Note).all()
    return render_template('notes.html', notes=my_notes, user = a_user)


@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = db.session.query(User).filter_by(email='dshelt10@uncc.edu').one()

    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note = my_note, user=a_user)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    a_user = {'name': 'Duane', 'email':'dshelt10@uncc.edu'}
    
    if request.method == 'POST':
        title = request.form['title']

        text = request.form['noteText']

        from datetime import date
        today = date.today()

        today = today.strftime("%m-%d-%Y")

        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('get_notes', user = a_user))

    else:  
        a_user = db.session.query(User).filter_by(email='dshelt10@uncc.edu').one()
        return render_template('new.html', user=a_user)


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.