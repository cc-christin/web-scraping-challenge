## Step 2 - MongoDB and Flask Application

# Imports
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
import scrape_mars

# flask app
app = Flask(__name__)

# flask_pymongo connection setup
app.config['MONGO_URI']= "mongodb://localhost:27017/mars_db"
mongo=PyMongo(app)

# Routes
@app.route("/")

# index
def index():
    mars=mongo.db.mars_db.find_one()
    return render_template("index.html", mars_db=mars)

# scrape
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_db
    data = scrape_mars.scrape_all()
    mars.update_one({}, {"$set": data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)