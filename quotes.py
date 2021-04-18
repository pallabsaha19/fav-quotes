from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config settings that will enable the application to connect with the database and interact with it
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/quotes'
# event notification system, it is used to track modification in alchemy sessions and this can take alot of resources therefore we will dissable it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# create a instance of alchemy and pass the app in it
db = SQLAlchemy(app)

# creating a class to make a table in the database
class Favquotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))


# end point for home page
@app.route('/')
def index():
    # fetch all the records from the database and store it in a result variable
    result = Favquotes.query.all()
    # to pass variables into the html template so that we can see it on html page, we have to pass a variable
    return render_template('index.html', result=result)


@app.route('/quotes')
def quotes():
    return render_template('quotes.html')


@app.route('/process', methods=['POST'])
def process():
    # create variable to capture the data entered by the user
    author = request.form['author']
    quote = request.form['quote']

    # create a variable that will store form inputs
    quotedata = Favquotes(author=author, quote=quote)
    # add that data to database session
    db.session.add(quotedata)
    # commit yo the database
    db.session.commit()

    # one the form has been submitted, I want user should be redirected to the home page
    return redirect(url_for('index'))


app.run(debug=True)