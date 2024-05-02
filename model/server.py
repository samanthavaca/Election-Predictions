from flask import Flask, jsonify
from flask_cors import CORS
import code_3

app = Flask(__name__)
# ... rest of your Flask code
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/votes')
def get_votes():
    # Replace this with real data fetching logic
    dem_votes = code_3.get_dem_votes(2020)
    rep_votes = code_3.get_rep_votes(2020)
    data = {
        "democratic": dem_votes,
        "republican": rep_votes,
        "threshold": 270
    }
    return jsonify(data)

@app.route('/votes2024')
def get_votes_2024():
    # Replace this with real data fetching logic
    dem_votes = code_3.get_dem_votes(2024)
    rep_votes = code_3.get_rep_votes(2024)
    data = {
        "democratic": dem_votes,
        "republican": rep_votes,
        "threshold": 270
    }
    return jsonify(data)

@app.route('/democratic')
def get_democratic_results():
    dem_results = code_3.get_dem_results(2020)
    return jsonify(dem_results)

@app.route('/republican')
def get_republican_results():
    rep_results = code_3.get_rep_results(2020)

    return jsonify(rep_results)

@app.route('/democratic2024')
def get_democratic_results_2024():
    dem_results = code_3.get_dem_results(2024)
    return jsonify(dem_results)

@app.route('/republican2024')
def get_republican_results_2024():
    rep_results = code_3.get_rep_results(2024)

    return jsonify(rep_results)

@app.route('/liberal')
def get_liberal_results():
    data = code_3.get_lib_results()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
