from flask import Blueprint, jsonify
import logging
from config.db_configs import db_configs, queries, fetch_rankings
from config import cache

get_ranking_bp = Blueprint('get_ranking', __name__)

@get_ranking_bp.route('/getRanking', methods=['GET'])
@cache.cached(timeout=86400)  # Cache this view for 24 hours
def get_ranking():
    all_rankings = {}
    for server, db_config in db_configs.items():
        if server == 'UAE':
            current_query = queries['UAE']
            before_query = queries['UAE_before']
        else:
            current_query = queries['default']
            before_query = queries['before']

        # Fetch current rankings
        logging.debug(f"Fetching current rankings for server: {server}")
        current_rankings = fetch_rankings(db_config, current_query)
        logging.debug(f"Current rankings for server {server}: {current_rankings}")
        all_rankings[server] = current_rankings
        print(f"Current rankings for server {server}: {current_rankings}")

        # Fetch before rankings
        logging.debug(f"Fetching before rankings for server: {server}")
        before_rankings = fetch_rankings(db_config, before_query)
        logging.debug(f"Before rankings for server {server}: {before_rankings}")
        all_rankings[f"{server}_before"] = before_rankings
        print(f"Before rankings for server {server}: {before_rankings}")

    response_json = jsonify(all_rankings)
    response_json.headers.add("Access-Control-Allow-Origin", "*")
    
    # Print the response to the console
    print("Final Response:", response_json.get_json())
    logging.debug(f"Response: {response_json.get_json()}")
    
    return response_json
