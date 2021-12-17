from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from flask import Flask, jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mondb = mongo.db

@app.route("/")
def index():
    mars = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars)

@app.route("/scrape")
def scraper():
    dmars = mondb.mars_data
    marsdata = scrape_mars.scrape_all()
    dmars.update_one({}, {"$set": marsdata}, upsert=True)
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run(debug=True)
