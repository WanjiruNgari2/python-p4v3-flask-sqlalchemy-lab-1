from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Route to get an earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def earthquakes(id):
    earthquake = db.session.get(Earthquake, id) 
    if not earthquake:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)
    return make_response(earthquake.to_dict(), 200)

# Route to create a new earthquake
@app.route('/earthquakes', methods=['POST'])
def create_earthquake():
    data = request.get_json()
    earthquake = Earthquake(**data)
    db.session.add(earthquake)
    db.session.commit()
    return make_response(earthquake.to_dict(), 201)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET']) 
# take a float as a parameter, get all with less than or equal to that magnitude and return the count of matching
# rows and a list of each row
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)

    return make_response({'count': count, 
                          'quakes': [e.to_dict() for e in earthquakes]}, 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
