from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from scrape_mars import scrape
import pymongo
from flask import Flask, jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.data.find_one()
    return render_template("index.html", data=mars_data)

@app.route("/scrape")
def scrapper():
    mars = mongo.db.data
    mars_data2 = scrape_mars.scrape_all()
    mars.update_one({}, mars_data2, upsert=True)
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run()
