from flask import Flask, request, jsonify, abort
import pyodbc
from flask_caching import Cache
from dotenv import load_dotenv
import os
import logging
import json

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
    Rank BETWEEN 1 AND 25;
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
    # Validate the presence of JSON in the request
    if not request.json:
        abort(400, 'No JSON payload received')

    try:
        # Validate the structure of the JSON data
        data_object = request.json.get('data', {}).get('object')
        if not data_object:
            abort(400, 'Malformed JSON: missing required "data.object" keys')

        # Check for custom fields and validate it is a list
        custom_fields = data_object.get('custom_fields')
        if not isinstance(custom_fields, list):
            abort(400, 'Missing or incorrect "custom_fields" in checkout session')

        # Define possible keys to look for the dropdown field
        dropdown_keys = ['region', 'server']
        dropdown_field = next((field for field in custom_fields if field['key'] in dropdown_keys and 'dropdown' in field), None)

        # Extract the dropdown value if the correct structure is found
        if dropdown_field and 'value' in dropdown_field['dropdown']:
            dropdown_value = dropdown_field['dropdown']['value']
        else:
            dropdown_value = 'Dropdown value not specified or incorrectly structured'

        return jsonify({'dropdown_value': dropdown_value})
    
    except KeyError as e:
        logging.error(f"Key error in processing the webhook: {str(e)}")
        abort(400, f"Key error: {str(e)}")
    except TypeError as e:
        logging.error(f"Type error in processing the webhook: {str(e)}")
        abort(400, f"Type error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500, f"Unexpected server error: {str(e)}")

@app.route('/')
def index():
    return "Welcome to the Ranking API! Use /getRanking to get the rankings."

@app.route('/getRanking', methods=['GET'])
@cache.cached(timeout=300)  # Cache this view for 5 minutes
def get_ranking():
    all_rankings = {}
    for server, db_config in db_configs.items():
        all_rankings[server] = fetch_rankings(db_config)

    response = jsonify(all_rankings)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
