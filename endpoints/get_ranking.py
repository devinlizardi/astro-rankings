from flask import Blueprint, jsonify
import logging
from config.db_configs import db_configs, queries, fetch_rankings, MovementType
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

        # Fetch before rankings
        logging.debug(f"Fetching before rankings for server: {server}")
        before_rankings = fetch_rankings(db_config, before_query)

        before_rankings_indexed_by_id = {ranking.uiID1: ranking for ranking in before_rankings}
        print(f'before_rankings_indexed_by_id = {before_rankings_indexed_by_id}')
        logging.debug(f"Before rankings for server {server}: {before_rankings}")

        for current_ranking in current_rankings:
            current_rank = current_ranking.Rank

            if current_ranking.uiID1 not in before_rankings_indexed_by_id:
                # If they were not on the leaderboards yesterday, but are today, then they must have moved up
                current_ranking.MovementType = MovementType.UP
                continue

            before_ranking = before_rankings_indexed_by_id[current_ranking.uiID1]

            if current_rank > before_ranking.Rank:
                current_ranking.MovementType = MovementType.UP
            elif current_rank < before_ranking.Rank:
                current_ranking.MovementType = MovementType.DOWN
            else:
                current_ranking.MovementType = MovementType.UNCHANGED

        all_rankings[server] = current_rankings
        all_rankings[f'{server}_before'] = before_rankings

    response_json = jsonify(all_rankings)
    response_json.headers.add("Access-Control-Allow-Origin", "*")

    # Print the response to the console
    print("Final Response:", response_json.get_json())
    logging.debug(f"Response: {response_json.get_json()}")

    return response_json
