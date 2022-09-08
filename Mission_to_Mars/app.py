import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Setup Flask
app = Flask(__name__)

# Connect to MongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_data = mongo.db.mars_data

# Route to create template
@app.route("/")
def home():

    return render_template("index.html")

# Route to scrape function
@app.route("/scrape")
def scrape():

    scraped_data = scrape_mars.scrape()
    mars_data.update({}, scraped_data, upsert=True)
    return redirect("/data")

# Route to page that pulls data from MongoDB
@app.route("/data")
def data():

    mars_info = mongo.db.mars_data.find_one()
    return render_template("data.html", info=mars_info)


if __name__ == "__main__":
    app.run(debug=True)