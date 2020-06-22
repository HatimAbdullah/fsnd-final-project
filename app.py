
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  @cross_origin()
  def welcome():
    return jsonify({'message':'this shit works'})

  @app.route("/actors", methods=['POST'])
  def add_actor():
    actor_info = request.get_json()
    print(actor_info)
    if not ('name' in actor_info and 'age' in actor_info and 'gender' in actor_info and 'movies' in actor_info):
      abort(422)
    print('g')
    actor_name = actor_info.get('name')
    actor_age = actor_info.get('age')
    actor_gender = actor_info.get('gender')
    actor_movies = actor_info.get('movies')

    #try:
    actor = Actor(name=actor_name, gender=actor_gender, age=actor_age, movies=actor_movies)
    actor.insert()

    return jsonify({
      'success': True,
      'created_with_id': actor.id,
      })

    #except:
     # abort(422)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
