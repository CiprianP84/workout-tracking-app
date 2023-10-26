# the main.py file deals with the CRUD, showing the homepage, profile page features
from . import db
from .models import User, Workout
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user



main = Blueprint('main', __name__) # we create a blueprint to make our project more modular and organised

# we create and define our page(s)
@main.route('/') # setting the route to page(s)
def index():
    return render_template('index.html') # rendering the page(s)


@main.route('/profile') 
@login_required  # this decorator checks if user is logged in or not before accessing the page
def profile():
    return  render_template('profile.html', name=current_user.name) 


@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')


@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    reps = request.form.get('reps')
    comment = request.form.get('comment')
    weight = request.form.get('weight')
    exercise = request.form.get('exercise')
    sets = request.form.get('sets')

    workout = Workout(weight=weight, exercise= exercise, sets=sets, reps=reps, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    flash('Your workout has been added!')

    return redirect(url_for('main.user_workouts'))

@main.route('/all')
@login_required
def user_workouts():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=3)
    return render_template("all_workouts.html", workouts=workouts, user=user)

@main.route("/workout/<int:workout_id>/update", methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.reps = request.form['reps']
        workout.comment = request.form['comment']
        workout.weight = request.form['weight']
        workout.exercise = request.form['exercise']
        workout.sets = request.form['sets']
        db.session.commit()
        flash('Workout updated successfully')
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html', workout=workout)


@main.route("/workout/<int:workout_id>/delete", methods=['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully')
    return redirect(url_for('main.user_workouts'))