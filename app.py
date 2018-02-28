from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_collection

    

@app.route('/')
def index():
    mars_info = db.mars_collection.find_one()
    return render_template('index.html', mars_news=mars_info)


@app.route('/scrape')
def scrape():
    mars_collection = db.mars_collection
    data = scrape_mars.scrape()
    mars_collection.update({}, data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)