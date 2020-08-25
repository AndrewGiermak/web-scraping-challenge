from flask import Flask, jsonify
import scrape_mars
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_dict

# create an instance of Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    mars_dict = db.mars_dict.find()
    # List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/scrape"
    )


@app.route("/scrape")
def web_scraper():
    scrape_mars.scrape();
    db.mars_dict.insert(scrape_mars.scrape())
    return jsonify(scrape_mars.scrape())


if __name__ == '__main__':
    app.run(debug=True)
