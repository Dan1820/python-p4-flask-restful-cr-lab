#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list=[]
        for plant in plants:
            plant_list.append({
                'id': plant.id,
                'name':plant.name,
                'name':plant.name,
                'image':plant.image,
                'price':float(plant.price)
            })

        return jsonify(plant_list)
    
    def post(self):
        data= request.get_json()
        name=data.get('name')
        image=data.get('image')
        price=data.get('price')

        if not name or not image or not price:
            return make_response(jsonify({'errror': 'Missing required fields'}),400)
        plant = Plant(name=name,image=image,price=float(price))
        db.session.add(plant)
        db.session.commit()
        return  jsonify({
            'id': plant.id,
            'name':plant.name,
            'name':plant.name,
            'image':plant.image,
            'price':float(plant.price)
            
        }),201
        
            

class PlantByID(Resource):
    def get (self,plant_id):
        plant = Plant.query.get(plant_id)

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}),404)
        
        plant_data={
            'id': plant.id,
            'name':plant.name,
            'name':plant.name,
            'image':plant.image,
            'price':float(plant.price)

        }
        return jsonify(plant_data)
    
    api.add_resource(Plants,'/plants')
    api.add_resource(PlantByID,'/plants/<int:plant_id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
