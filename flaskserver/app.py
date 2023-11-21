from flask import Flask, request, jsonify
import json
import requests
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['ENV'] = 'production'
app.config['DEBUG'] = False

quiz_structure = {}
user_genres = []

def load_quiz_structure():
    global quiz_structure
    with open('structure.json', 'r') as f:
        quiz_structure = json.load(f)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/quiz', methods=['GET'])
def get_quiz_res():
    quiz_response = request.args.get('quiz', 'No response')
    quiz_dict = json.loads(quiz_response)

    global user_genres
    for ques in quiz_dict:
        user_res = quiz_dict[ques]
        genres_list = quiz_structure[ques]["options"][user_res]["genres"]
        for genre in genres_list:
            if genre["id"] not in user_genres:
                user_genres.append(genre["id"])
    
    user_movies_all = get_movies(user_genres=user_genres)
    user_movies_list = user_movies_all["results"]

    chosen_movie_ids = set()
    user_movies = []
    while len(user_movies) < 3:
        movie = random.choice(user_movies_list)
        if movie['id'] not in chosen_movie_ids:
            chosen_movie_ids.add(movie['id'])
            user_movies.append(movie)

    return jsonify({'user_movies': user_movies})
def get_movies(user_genres):

    url = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_original_language=en&with_genres="

    for i in range(0, len(user_genres)):
        url += f"{user_genres[i]}%7C"
    # print(url)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlOGViODVkNDExYjI0Yzg4MjdiYjdlOTY4ZTRkYmY5MSIsInN1YiI6IjY1NDRjODViZmQ0ZjgwMDBlNDdlOTU1NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.k_qMdzhZwBgmncIZjP70uvM89A3Wc_n_zXZxSH8uVXY"
    }

    response = requests.get(url, headers=headers)

    return response.json()


if __name__ == '__main__':
    load_quiz_structure()
    app.run(host='0.0.0.0', port=5000)

# get request - http://127.0.0.1:5000/quiz?quiz={"QID101":"b","QID102":"b","QID103":"b"}
