from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient
import pymongo
import os

# create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 
    # find data in dict
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# route for the scrape functions
@app.route("/scrape")
def scrape(): 
    # run functions
    mars_dict = mongo.db.mars_dict
    mars_web = scrape_mars.scrape_news()
    mars_web = scrape_mars.scrape_image()
    mars_web = scrape_mars.scrape_facts()
    mars_web = scrape_mars.scrape_hemispheres()

    # Update the Mongo Database using update and upsert=True
    mars.update({}, mars_web, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


    
