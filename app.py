from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
from utils import *

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect("/sem_search")


@app.route("/sem_search", methods = ["GET", "POST"])
def process():
    if(request.method == "GET"):
        return render_template("sem_search.html", res = "")
    
    
    query = request.form['query']
    query = query.strip()
    # if(query == ""):
    #     return render_template("sem_search.html", res = "Query cannot be empty")

    data = process_query(query)
    return render_template("sem_search.html", res = data)


if(__name__ == "__main__"):
    app.run(debug=True)