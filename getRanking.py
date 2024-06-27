from flask import Flask, request, jsonify, abort
import pyodbc
from flask_caching import Cache
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='app_errors.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection strings with parameters from environment variables
db_configs = {
    'NA': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("NA_DB_SERVER")};DATABASE={os.getenv("NA_DB_DATABASE")};UID={os.getenv("NA_DB_UID")};PWD={os.getenv("NA_DB_PASSWORD")}',
    'EU': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("EU_DB_SERVER")};DATABASE={os.getenv("EU_DB_DATABASE")};UID={os.getenv("EU_DB_UID")};PWD={os.getenv("EU_DB_PASSWORD")}',
    'UAE': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("UAE_DB_SERVER")};DATABASE={os.getenv("UAE_DB_DATABASE")};UID={os.getenv("UAE_DB_UID")};PWD={os.getenv("UAE_DB_PASSWORD")}',
    'TH': f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("TH_DB_SERVER")};DATABASE={os.getenv("TH_DB_DATABASE")};UID={os.getenv("TH_DB_UID")};PWD={os.getenv("TH_DB_PASSWORD")}'
}

# The query to run
query = """
SELECT 
    Rank,
    szID1,
    szID2,
    Value1,
    'https://static.latale.com/static/v3/web/img/character/character_' + 
    CASE 
        WHEN szID2 = 15 THEN '78'
        ELSE CAST(szID2 AS VARCHAR(10)) 
    END + 
    '.png' AS CharacterImageURL
FROM 
    tbluRanking
WHERE 
    Rank BETWEEN 1 AND 5;
"""

def fetch_rankings(db_config):
    try:
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
        return results
    except pyodbc.Error as e:
        logging.error(f"Error fetching rankings for config {db_config}: {e}")
        return []

@app.route('/webhook', methods=['POST'])
def webhook():
    if not request.json:
        abort(400)  # Abort if no JSON is received
    data = request.json
    try:
        # Extracting the region dropdown value
        checkout_session = data[0]['raw']['data']['object']
        custom_fields = checkout_session['custom_fields']
        region_value = next((item for item in custom_fields if item['key'] == 'region'), None)
        if region_value:
            region_value = region_value['dropdown']['value']
        else:
            region_value = 'Region not specified'
        return jsonify({'region': region_value})
    except (KeyError, TypeError) as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({'error': 'Error processing data'}), 500

@app.route('/')
def index():
    return "Welcome to the Ranking API! Use /getRanking to get the rankings."

@app.route('/getRanking', methods=['GET'])
@cache.cached(timeout=300)  # Cache this view for 5 minutes
def get_ranking():
    all_rankings = {}
    for server, db_config in db_configs.items():
        all_rankings[server] = fetch_rankings(db_config)
    return jsonify(all_rankings)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
