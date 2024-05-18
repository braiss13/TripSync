# Contenido generado por ChatGPT, ¡¡REVISAR!!

# views/score.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.Score import Score
from model.Trip import Trip
from model.User import User
import sirope

score_bp = Blueprint('scores', __name__)

@score_bp.route('/scores')
def index():
    s = sirope.Sirope()
    scores = list(s.load_all(Score))
    return render_template('scores/index.html', scores=scores)

@score_bp.route('/scores/add', methods=['GET', 'POST'])
def add_score():
    s = sirope.Sirope()
    if request.method == 'POST':
        trip_id = request.form['trip_id']
        user_id = request.form['user_id']
        rating = request.form['rating']

        # Verificar que el viaje y el usuario existan
        trip = s.find_first(Trip, lambda t: t.id == trip_id)
        user = s.find_first(User, lambda u: u.id == user_id)
        
        if trip and user:
            new_score = Score(trip_id, user_id, rating)
            s.save(new_score)
            return redirect(url_for('scores.index'))
        else:
            flash('Invalid trip ID or user ID')

    return render_template('scores/add_score.html')
