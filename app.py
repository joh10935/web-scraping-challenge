from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Setup Flask
app = Flask(__name__)

# Connect to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to create template
@app.route("/")
def index():

    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

# Route to scrape function
@app.route("/scrape")
def scraper():
  
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mongo.db.mars_dict.update_one({}, {"$set": mars_data}, upsert=True)
    # mars_dict.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)