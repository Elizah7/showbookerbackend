from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask import Flask, jsonify
from flask_cors import CORS
from bson.objectid import ObjectId

 # This enables CORS for all routes in the Flask app

# Your routes and other Flask code

app = Flask(__name__)
CORS(app) 
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this to a secure secret key in production
app.config['MONGODB_SETTINGS'] = {'host':"mongodb+srv://uddeshiv:uddeshiv@cluster0.5xu2vfk.mongodb.net/showbooker?retryWrites=true&w=majority"}
jwt = JWTManager(app)

# Initialize MongoDB client
client = MongoClient(app.config['MONGODB_SETTINGS']['host'])
db = client.get_database()

# User Route - Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    phone_number = data["phone_number"]
    # Check if the username or email already exists
    if db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
        return jsonify({'message': 'Username or email already exists'}), 400

    # Create a new user document
    new_user = {
        'username': username,
        'email': email,
        'password': password,
        'phone_number':phone_number
    }
    db.users.insert_one(new_user)

    return jsonify({'message': 'User created'})

# User Route - Login
@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    # Check if the user exists
    user = db.users.find_one({'username': username})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate and return the access token
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'access_token': access_token})

# User Route - Get Current User
@app.route('/users/me', methods=['GET'])
@jwt_required
def get_current_user():
    current_user_id = get_jwt_identity()
    user = db.users.find_one({'_id': current_user_id})
    return jsonify({'username': user['username'], 'email': user['email']})



@app.route('/data', methods=['GET'],endpoint='get_movie')
def get_movie():
    query_param = request.args.get('category')
   
    movie = db.movies.find({'category':query_param})
    if movie is None:
        return jsonify({'message': 'Movie not found'}), 404

    # Return the movie
    movie_data  = []

    for entry in movie :
        if entry['category'] == "movie" :
            print(entry["_id"])
            movie_dict = {
              "_id": str(entry["_id"]),
              "title" : entry['title'],
              "description" : entry['description'],
              "timings" : entry['timings'],
              "ratings" : entry['ratings'],
              "cast" : entry['cast'],
              "director" : entry['director'],
              "language" : entry['language'],
              "release_date" : entry['release_date'],
              "image" : entry['image'],
              "category" : entry["category"],
            }

            movie_data.append(movie_dict)
        elif entry['category'] == "comedyshow" :
            movie_dict = {
              "id":entry["_id"],
              "title" : entry['title'],
              "artist" : entry['artist'],
              "timing" : entry['timing'],
              "duration" : entry['duration'],
              "venue" : entry['venue'],
              "price" : entry['price'],
              "about" : entry['about'],
              "image" : entry['image'],
              "category" : entry["category"],
            }
            movie_data.append(movie_dict)    
    return jsonify({"movies":movie_data})        
     

# title
# "Uncle Roger Live"
# artist
# "Uncle Roger"
# timing
# "8:45 PM"
# venue
# "The Laugh House"
# price
# 320
# about
# "Get ready for a laughter-filled night with Uncle Roger"
# duration
# "2 hours"
# image
# "https://i.guim.co.uk/img/media/11ef3efe6d7d5196634df7f557784e621ce39da…"
# category
# "comedyshow"

@app.route('/data/<movie_id>', methods=['GET'],endpoint='get_single_movie')
def get_single_movie(movie_id):
    # Find the movie by ID
      movie = db.movies.find_one({'_id': ObjectId(movie_id)})

      if movie is None:
        return jsonify({'message': 'Movie not found'}), 404

      movie_data = {
        "_id": str(movie["_id"]),  # Convert ObjectId to a string for JSON serialization
        "title": movie['title'],
        "description": movie['description'],
        "timings": movie['timings'],
        "ratings": movie['ratings'],
        "cast": movie['cast'],
        "director": movie['director'],
        "language": movie['language'],
        "release_date": movie['release_date'],
        "image": movie['image'],
        "category": movie["category"],
    }

      return jsonify(movie_data)



# Movie Route - Create Movie
@app.route('/data/create', methods=['POST'],endpoint='create_movie')
@jwt_required
def create_movie():
    data = request.json
    category = data["category"]
    if category=="movie" :
        title = data['title']
        description = data['description']
        timings = data['timings']
        ratings = data['ratings']
        cast = data['cast']
        director = data['director']
        language = data['language']
        release_date = data['release_date']
        image = data['image']
        category = data["category"]
        ticket_price = data["ticket_price"]
        category=="movie"
        new_movie = {
        title,
        description,
        timings,
        ratings,
        cast,
        director,
        language,
        release_date,
        image,
        category,
        ticket_price
        }
        db.movies.insert_one(new_movie)
    elif category == "comdey_shows" :
        artist = data['artist']
        title = data['title']
        about = data['about']
        timing = data['timings']
        venue = data['venue']
        cast = data['cast']
        director = data['director']
        language = data['language']
        release_date = data['release_date']
        image = data['image']
        category = data["category"]
        price = data["price"]
        category=="movie"
        new_movie = {
        artist,
        title,
        about,
        timing,
        venue,
        cast,
        director,
        language,
        release_date,
        image,
        category,
        price
        }
        db.movies.insert_one(new_movie)  

  

    return jsonify({'message': 'Movie created'})

# _id
# 64bf727dbd02c08c8a33e835
# title
# "Uncle Roger Live"
# artist
# "Uncle Roger"
# timing
# "8:45 PM"
# venue
# "The Laugh House"
# price
# 320
# about
# "Get ready for a laughter-filled night with Uncle Roger"
# duration
# "2 hours"
# image
# "https://i.guim.co.uk/img/media/11ef3efe6d7d5196634df7f557784e621ce39da…"
# category
# "comedyshow"
# Movie Route - Update Movie
@app.route('/data/<movie_id>', methods=['PATCH'],endpoint='update_movie')
@jwt_required
def update_movie(movie_id):
    print(movie_id)
    data = request.json
    rating_arr = []
    print(rating_arr)
    rating = data['rating']
    print(rating)
    # Find the movie by ID
    movie = db.movies.find({'_id': ObjectId(movie_id)})
    print(movie)
    if movie is None:
        return jsonify({'message': 'Movie not found'}), 404
    
    # Update the movie details

    for entry in movie:
       rating_arr = entry['ratings']
    
    rating_arr.append(rating)
    db.movies.update_one({
        '_id': movie_id
    }, {
        '$set': {
            'ratings': rating_arr
        }
    })
    return jsonify({'message':"movie has been updated"})


@app.route('/data/<movie_id>', methods=['DELETE'],endpoint='delete_movie')
@jwt_required
def delete_movie(movie_id):
    # Find the movie by ID
    movie = db.movies.find_one({
        '_id': movie_id
    })

    if movie is None:
        return jsonify({'message': 'Movie not found'}), 404

    # Delete the movie
    db.movies.delete_one({
        '_id': movie_id
    })

    return jsonify({'message': 'Movie deleted'})



   


if __name__ == '__main__':
    app.run(debug=True)
