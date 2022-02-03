from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drinks(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique= True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} | {self.description}"

@app.route('/')
def index():
    return "Hello world!"

@app.route('/drinks')
def get_drinks():
    drinks = Drinks.query.all()
    output = []
    for drink in drinks:
        drinks_data = {'name':drink.name, 'description':drink.description}
        output.append(drinks_data)
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drinks.query.get_or_404(id)
    return {"name":drink.name, "description":drink.description}

@app.route('/drinks', methods=['POST'])

def add_drink():
    drink = Drinks(name = request.json['name'], description = request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id}

@app.route('/drinks/<id>',  methods=['DELETE'])    
def delete_drink(id):
    drink = Drinks.query.get(id)
    if drink is None:
        return {"error":"Drink was not found!"}
    db.session.delete(drink)
    db.session.commit()
    return {"message":f'Drink {drink.name} deleted'}