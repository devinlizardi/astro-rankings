from flask import Blueprint, request, jsonify, abort
import logging

addCash_bp = Blueprint('addCash', __name__, url_prefix='/addCash')

SECRET = "dsadasxcfe3e32ezaxdsad3aSG"

@addCash_bp.route('/', methods=['POST'])  # Adjusted to just '/' since 'url_prefix' handles '/addCash'
def add_cash():
    secret = request.json.get('secret')
    account_name = request.json.get('account_name')
    server = request.json.get('server')
    cash_value = request.json.get('cash_value')

    # Authenticating the secret key
    if secret != SECRET:  # It's better to use the SECRET constant you defined
        return jsonify({'error': 'Unauthorized'}), 403

    # Database connection parameters
    if server == 'NA':
       connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('NA_DB_SERVER')};DATABASE={os.getenv('NA_DB_CASH_DATABASE')};UID={os.getenv('NA_DB_UID')};PWD={os.getenv('NA_DB_PASSWORD')}"
    elif server == 'UAE':
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('UAE_DB_SERVER')};DATABASE={os.getenv('UAE_DB_CASH_DATABASE')};UID={os.getenv('UAE_DB_UID')};PWD={os.getenv('UAE_DB_PASSWORD')}"
    else:
        return jsonify({'error': 'Invalid server selection'}), 400

    # Execute the stored procedure
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("{CALL usp_AddCash(?, ?, ?)}", (account_name, cash_value, "BTC"))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Cash added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
