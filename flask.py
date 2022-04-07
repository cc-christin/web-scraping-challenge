## Step 2 - MongoDB and Flask Application

# Imports
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# flask app
app = Flask(__name__)

# flask_pymongo connection setup
app.config['MONGO_URI']= "mongodb://localhost:27017/mars"
mongo=PyMongo(app)

# Routes
@app.route("/")

# index
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# scrape
def scrape():
    mars=mongo.db.mars
    data = scraping.scrape_all()
    mars.update({}, data, upsert=True)
    return "Finsihed Scraping"

if __name__ == "__main__":
    app.run(debug=True)