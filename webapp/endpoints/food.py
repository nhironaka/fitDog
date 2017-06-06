from flask import request, jsonify

from webapp.models import FoodLog, Food, Log
from webapp import application, db
from helpers import get_date

import os
import json

@application.route('/food/all', methods=['POST'])
def get_foods():
    foodList = []
    try:
        foods = Food.query.all()
        
        for food in foods:
            foodList.append(food.to_json())

        return json.dumps(foodList)

    except Exception, e:
        return json.dumps(str(e))

@application.route('/food/new', methods=['POST'])
def add_new_food():
    try:
        json_data = request.json
        food_name = json_data.get('food')
        calories = json_data.get('calories', 0)
        serving = json_data.get('serving', 0)
        print food_name, calories, serving
        similar = Food.query.filter(Food._name==food_name, Food._calories==calories).first();
        if similar is None:
            food = Food(food_name, calories, serving)
            db.session.add(food)
            db.session.commit()
            return json.dumps(food.to_json())

        return json.dumps({
            'message': 'You already have a food called ' + food_name + '.'    
        })
    except Exception, e:
        return json.dumps(str(e)), 500

@application.route('/log/food/update', methods=['POST'])
def update_food_log():
    try:
        food_log = request.json.get('foodLog')
        food_log_id = food_log.get('id')
        if food_log_id is None:
            dog_id = request.json.get('id')
            log_date = get_date(request.json.get('date'))
            log = Log.query.filter(Log.dog_id==dog_id, Log._date==log_date).first()
            if log is None:
                log = Log(log_date, dog_id);
                db.session.add(log)
                db.session.commit()
            return add_food_log(log.id, food_log)
        else:
            edit_food_log(food_log)

    except Exception, e:
        raise e

def add_food_log(log_id, log):
    try:
        food_log = FoodLog(log.get('amount'), log.get('foodId'), log_id)
        db.session.add(food_log)
        db.session.commit()

        food = Food.query.filter(Food.id==log.get('foodId')).first()
        food_item = {
            'amount': food_log._amount,
            'name': food._name,
            'calories': round(food._calories * food_log._amount / food._serving),
            'foodId': food.id,
            'id': food_log.id
        }
        return json.dumps(food_item)
    except Exception, e:
        raise e;

def edit_food_log(log):
    try:
        food_log = FoodLog.query.filter_by(id=log.get('id')).first()
        food_log._calories = log.get('calories', food_log._duration)
        food_log._amount = log.get('amount', food_log._intensity)
        food_log.food_id = log.get('foodId', food_log.food_id)
        db.session.add(food_log)
        db.session.commit()
        return json.dump(food_log.to_json())
    except Exception, e:
        raise e;

@application.route('/log/food/delete', methods=['POST'])
def delete_food_log():
    try:
        food_log_id = request.json.get('id')
        food_log = FoodLog.query.filter_by(id=food_log_id).first()
        
        db.session.delete(food_log)
        db.session.commit()
        return json.dumps({
            'message': 'Successfully deleted'
        })

    except Exception, e:
        return json.dumps(str(e))