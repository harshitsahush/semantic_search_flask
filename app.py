from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
from utils import *   


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect("/sem_search")

@app.route("/sem_search", methods = ["GET", "POST"])
def process():

    if(request.is_json):
        query = request.args.get('query_text')
        print(query)
        if(query):
            query = query.strip()
            data = process_query(query)
            #need to data in a html table code
            data = html_table(data)
            return data
    
    return render_template("sem_search.html")


if(__name__ == "__main__"):
    app.run(debug=True)