from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

sqlConn = sqlite3.connect('movie-app\movie.db', check_same_thread=False)
sqlCursor = sqlConn.cursor()

if sqlConn:
    print("connection success")

# table = 'CREATE TABLE IF NOT EXISTS users(u_id INTEGER PRIMARY KEY, u_name TEXT);'
# sqlCursor.execute(table)
      
# table = 'CREATE TABLE IF NOT EXISTS movies(m_id INTEGER PRIMARY KEY ,m_name TEXT, m_year INTEGER );'
# sqlCursor.execute(table)

# table = 'CREATE TABLE IF NOT EXISTS reviews(r_id INTEGER PRIMARY KEY, review TEXT);'
# sqlCursor.execute(table)
    
# sqlCursor.execute("DROP TABLE IF EXISTS reviews")

# movies = [
#     {"m_name": "mov2", "m_year": "2012"}
# ]

# users = [
#     {"u_name": "user1"}
# ]

# reviews = [
#     {"review": "good movie"}
# ]

# Route to render index html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addMovie', methods=['POST'])
def addMovie():
    return render_template('addMovie.html')

@app.route('/addReview', methods=['POST'])
def addReview():
    return render_template('reviewMovie.html')

# Route to get all movies:  WORKING
@app.route('/movie', methods=['GET'])
def get_movies():
    sqlCursor.execute("SELECT * FROM movies")
    movies = sqlCursor.fetchall()
    return jsonify(movies)

# Route to get all reviews: WORKING
@app.route('/review', methods = ['GET'])
def get_reviews():
    sqlCursor.execute("SELECT * FROM reviews")
    reviews = sqlCursor.fetchall()
    return jsonify(reviews)

# Route to get all users:   WORKING
@app.route('/users', methods=['GET'])
def get_users():
    sqlCursor.execute("SELECT * FROM users")
    users = sqlCursor.fetchall()
    return jsonify(users)

# Route to get a specific movie by ID:  WORKING
@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    sqlCursor.execute("SELECT * FROM movies WHERE m_id = ?", (movie_id,))
    movie_data = sqlCursor.fetchone()
    if movie_data is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie_data)

# Route to create a new movie:  WORKING
@app.route('/movie', methods = ['POST'])
def create_movie():
    # if not request.json or 'm_name' not in request.json or 'm_year' not in request.json:
    #     abort(400)
    m_name = request.form['m_name']
    m_year = request.form['m_year']
    # data = request.form()
    sqlCursor.execute("INSERT INTO movies (m_name, m_year) VALUES (?, ?)", (m_name, m_year))
    sqlConn.commit()
    # return jsonify({'message': 'Movie added successfully'})
    return render_template('movieSuccess.html')

# Route to create a new review: WORKING
@app.route('/review', methods = ['POST'])
def create_review():
    if not request.json or 'review' not in request.json:
        abort(400)
    data = request.json
    sqlCursor.execute("INSERT INTO reviews (review) VALUES (?)", (data['review'],))
    sqlConn.commit()
    return jsonify({'message': 'Review added successfully'})

# Route to create a new user:   WORKING
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or 'u_name' not in request.json:
        abort(400)
    data = request.json
    sqlCursor.execute("INSERT INTO users (u_name) VALUES (?)", (data['u_name'],))
    sqlConn.commit()
    return jsonify({'message': 'User created successfully'})

# # Route to update an existing movie by ID
# @app.route('/movie/<int:movie_id>', methods=['PUT'])
# def update_movie(movie_id):
#     movie = next((movie for movie in movies if movie['mid'] == movie_id), None)
#     if not movie:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'name' in request.json:
#         movie['name'] = request.json['name']
#     if 'year' in request.json:
#         movie['year'] = request.json['year']
#     return jsonify(movie)

# # Route to delete an existing movie by ID:  WORKING
# @app.route('/movie/<int:movie_id>', methods=['DELETE'])
# def delete_movie(movie_id):
#     movie = next((movie for movie in movies if movie['mid'] == movie_id), None)
#     if not movie:
#         abort(404)
#     movies.remove(movie)
#     return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
