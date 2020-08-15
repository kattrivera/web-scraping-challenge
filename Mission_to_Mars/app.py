from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_Mars 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_Mars.scrape_all()
    print(mars_data)
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
