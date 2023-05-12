from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase("drinks", 
                        user="MCDetritus", 
                        password="", 
                        host="localhost", 
                        port="5432")

class BaseModel(Model):
    class Meta:
        database = db

class Drink(BaseModel):
    name = CharField()
    method = CharField()
    spirit = CharField()

db.connect()
db.drop_tables([Drink])
db.create_tables([Drink])

Drink(name='Cosmopolitan', method='shaken', spirit='vodka').save()
Drink(name='Tom Collins', method='shaken', spirit='gin').save()
Drink(name='Daquiri', method='shaken', spirit='rum').save()
Drink(name='Paloma', method='shaken', spirit='tequila').save()
Drink(name='NY Sour', method='shaken', spirit='whiskey').save()
Drink(name='Negroski', method='stirred', spirit='vodka').save()
Drink(name='Bijou', method='stirred', spirit='gin').save()
Drink(name='El Presidente', method='stirred', spirit='rum').save()
Drink(name='Rosita', method='stirred', spirit='tequila').save()
Drink(name='Manhattan', method='stirred', spirit='whiskey').save()

app = Flask(__name__)

@app.route('/drinks/', methods=['GET', 'POST'])
@app.route('/drinks/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Drink.get(Drink.id == id)))
        else:
            drink_list = []
            for drink in Drink.select():
                drink_list.append(model_to_dict(drink))
            return jsonify(drink_list)
        
    if request.method == 'POST':
        new_drink = dict_to_model(Drink, request.get_json())
        new_drink.save()
        return jsonify({"success": True})
        
    if request.method == 'PUT':
        body = request.get_json()
        Drink.update(body).where(Drink.id == id).execute()
        return f"Drink {id} has been updated."
        
    if request.method == 'DELETE':
        Drink.delete().where(Drink.id == id).execute()
        return f"Drink {id} has been deleted"

@app.route("/")
def index():
    return "We don't have Red Bull."

app.run(port=8000, debug=True)