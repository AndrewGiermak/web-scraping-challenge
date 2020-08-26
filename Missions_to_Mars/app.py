from flask import Flask, jsonify, render_template, redirect 
import scrape_mars
from flask_pymongo import PyMongo
import os

# create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Run the scrape function

@app.route("/")
def welcome():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

# Run the scrape function

@app.route("/scrape")
def scraper():
    mars_dict = mongo.db.mars_dict
    mars_dict_data = scrape_mars.scrape_news()
    mars_dict_data = scrape_mars.scrape_image()
    mars_dict_data = scrape_mars.scrape_facts()
    mars_dict_data = scrape_mars.scrape_hemispheres()

    # Update the Mongo Database using update and upsert=True
    mars_dict.update({}, mars_dict_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)