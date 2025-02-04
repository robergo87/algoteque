import json
from os import getenv
from os.path import join as path_join, dirname, abspath

import werkzeug
from flask import Flask, request, Response, jsonify
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

CURR_DIR = dirname(abspath(__file__))

application = Flask(__name__)

SENTRY_DSN = getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN, integrations=[FlaskIntegration()])


def get_top_topics(content):
    return [
        {"name": row[0], "qty": row[1]}
        for row in 
        sorted(content.get("topics", {}).items(), key=lambda row: row[1], reverse=True)[0:3]
    ]


def load_conf_file():
    with open(path_join(CURR_DIR, "conf.json"), "r") as f:
        raw_conf = json.load(f)
        provider_by_topic = {}
        for provider, topics in raw_conf.get("provider_topics").items():
            topics = [topic.strip().lower() for topic in topics.split("+")]
            for topic in topics:
                if topic not in provider_by_topic:
                    provider_by_topic[topic] = set()
                provider_by_topic[topic].add(provider)
    return provider_by_topic
    
CONF_TOPICS = load_conf_file()


    
def get_provider_quotes(topics):
    providers_matching = {} # dict of sets of positions of topics found for provider
    for index, topic_row in enumerate(topics):
        for provider in CONF_TOPICS.get(topic_row["name"], set()):
            if provider not in providers_matching:
                providers_matching[provider] = set()
            providers_matching[provider].add(index)    
            
    def get_quote(provider_match):
        score = len(provider_match)
        if score == 1:
            if 0 in provider_match:
                return 0.2 * topics[0]["qty"]
            if 1 in provider_match:
                return 0.25 * topics[1]["qty"]
            if 2 in provider_match:
                return 0.30 * topics[2]["qty"]
        if score == 2: 
            base = sum([
                topic["qty"] for index, topic in enumerate(topics)
                if index in provider_match
            ])
            return 0.1*base
        if score == 3: # rare case when all 3 topics match
            return 0.1*(topics[0]["qty"]+topics[1]["qty"])
    
    return [
        {"provider": provider, "quote": get_quote(provider_match)}
        for provider, provider_match in providers_matching.items()
    ]


@application.errorhandler(werkzeug.exceptions.BadRequest)
def handle_400(e):
    return json.dumps({"status": "error", "message": "Malformed Request"}), 400

@application.errorhandler(werkzeug.exceptions.Unauthorized)
def handle_401(e):
    return json.dumps({"status": "error", "message": "You are not authorized to execute this request"}), 401

@application.errorhandler(werkzeug.exceptions.Forbidden)
def handle_403(e):
    return json.dumps({"status": "error", "message": "You are forbidden to execute such request"}), 403

@application.errorhandler(werkzeug.exceptions.NotFound)
def handle_404(e):
    return json.dumps({"status": "error", "message": "Requested resource was not found"}), 404

@application.errorhandler(Exception)
def handle_500(e):
    return json.dumps({"status": "error", "message": "Internal server error"}), 500


@application.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    

@application.post("/api/recommend/")
def api_recommend():
    content = request.get_json(silent=True)
    if not content:
        return Response("Invalid request format", status=400)
    topics = get_top_topics(content)
    return jsonify({"status": "success", "content": get_provider_quotes(topics)})
