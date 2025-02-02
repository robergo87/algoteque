from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    

@application.post("/api/recommend/")
def api_recommend():
    return "<p>Hello, World!</p>"