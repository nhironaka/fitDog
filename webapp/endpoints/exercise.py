from flask import request, jsonify

from webapp.models import ExerciseLog, Exercise, Log
from webapp.helpers import get_date
from webapp import application, db

import os
import json

@application.route('/exercise/all', methods=['POST'])
def get_exercises():
    exerciseList = []
    try:
        activities = Exercise.query.all()
        for activity in activities:
            exerciseList.append(activity.to_json())
        return json.dumps(exerciseList)
    except Exception, e:
        return json.dumps(str(e))

@application.route('/exercise/new', methods=['POST'])
def add_new_exercise():
    try:
        json_data = request.json
        activity = json_data.get('activity')
        description = json_data.get('description', '')
        similar = Exercise.query.filter(Exercise._name==activity, Exercise._description==description).first()
        if similar is None:
            exercise = Exercise(activity, description)
            db.session.add(exercise)
            db.session.commit()
            return json.dumps({
                'message': 'Successfully added' + activity,
                'status': 'success',
                'exercise': exercise.to_json()
            })
        return json.dumps({
            'message': 'You already have an activity called ' + activity + '.',
            'status': 'info'
        })
    except Exception, e:
        return json.dumps({
            'message': str(e),
            'status': 'error'
        }), 500

@application.route('/log/exercise/update', methods=['POST'])
def update_exercise_log():
    try:
        exercise_log = request.json.get('exerciseLog')
        exercise_log_id = exercise_log.get('id')
        if exercise_log_id is None:
            dog_id = request.json.get('id')
            log_date = get_date(request.json.get('date'))
            log = Log.query.filter(Log.dog_id==dog_id, Log._date==log_date).first()
            if log is None:
                log = Log(log_date, dog_id)
                db.session.add(log)
                db.session.commit()
            return add_exercise_log(log.id, exercise_log)
        else:
            return edit_exercise_log(exercise_log)

    except Exception, e:
        return json.dumps({
            'message': str(e),
            'status': 'error'
        }), 500

def add_exercise_log(log_id, log):
    try:
        exercise_log = ExerciseLog(log.get('duration', 0), log.get('exerciseId'), log_id)
        db.session.add(exercise_log)
        db.session.commit()
        exercise = Exercise.query.filter(Exercise.id==exercise_log.exercise_id).first()
        exercise_item = {
            'duration': exercise_log._duration,
            'name': exercise._name,
            'description': exercise._description,
            'exerciseId': exercise.id,
            'id': exercise_log.id
        }
        return json.dumps(exercise_item)
    except Exception, e:
        raise e

def edit_exercise_log(log):
    try:
        exercise_log = ExerciseLog.query.filter_by(id=log.get('id')).first()
        exercise_log._duration = log.get('duration', exercise_log._duration)
        exercise_log.exercise_id = log.get('exerciseId', exercise_log.exercise_id)
        db.session.add(exercise_log)
        db.session.commit()
        return json.dumps(exercise_log.to_json())
    except Exception, e:
        raise e

@application.route('/log/exercise/delete', methods=['POST'])
def delete_exercise_log():
    try:
        exercise_log_id = request.json.get('id')
        exercise_log = ExerciseLog.query.filter_by(id=exercise_log_id).first()
        
        db.session.delete(exercise_log)
        db.session.commit()
        return json.dumps({
            'message': 'Successfully deleted',
            'status': 'success'
        })

    except Exception, e:
        return json.dumps({
            'message': str(e),
            'status': 'error'
        }), 500
