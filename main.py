import requests
import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

API_KEY = os.environ['API_KEY']
FLASK_KEY = os.urandom(25)
URL = 'https://the-one-api.dev/v2/'

HEADER = {
    'Authorization': f'Bearer {API_KEY}',
          }

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_KEY
Bootstrap(app)


class CharacterSearch(FlaskForm):
    name = StringField('Character name')
    race = StringField('Race')
    gender = SelectField('Gender', choices=['', 'Male', 'Female'])
    submit = SubmitField('Submit')


class QuoteForm(FlaskForm):
    name = StringField('Character name')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CharacterSearch()
    if form.validate_on_submit():
        name = form.name.data
        race = form.race.data
        gender = form.gender.data
        parameters = {
            'name': name,
            'race': race,
            'gender': gender,
        }
        data_dict = requests.get(URL+'character', params=parameters, headers=HEADER).json()['docs']
        return render_template('characterProfile.html', names=data_dict)
    return render_template('index.html', form=form)


@app.route('/quotes', methods=["GET", 'POST'])
def search_quotes():
    form = QuoteForm()
    if form.validate_on_submit():
        name = form.name.data
        parameters = {
            'name': name,
        }
        character_id = requests.get(URL + 'character', params=parameters, headers=HEADER).json()['docs'][0]['_id']
        quote_dict = requests.get(URL + 'character/' + character_id + '/quote', params=parameters, headers=HEADER).json()['docs']
        return render_template('characterQuotes.html', quotes=quote_dict, name=name)
    return render_template('quote.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
