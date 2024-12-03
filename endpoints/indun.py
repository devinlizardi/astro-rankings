from flask import Blueprint, request, jsonify
import pyodbc
import logging
from config.db_configs import db_configs

indun_bp = Blueprint('indun', __name__)


@indun_bp.route('/indun', methods=['GET'])
def indun():
    char_name = request.args.get('CharName')
    region = request.args.get('region', 'NA')  # Default to 'NA' if region is not specified

    if not char_name:
        return jsonify({"error": "CharName parameter is required"}), 400

    if region not in db_configs:
        return jsonify({"error": "Invalid region specified"}), 400

    try:
        conn = pyodbc.connect(str(db_configs[region]))
        cursor = conn.cursor()
        cursor.execute("EXEC RetrieveIndun @CharName = ?", char_name)

        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        conn.close()

        response_json = jsonify(results)

        return response_json
    except pyodbc.Error as e:
        logging.error(f"Error fetching Indun data: {e}")
        return jsonify({"error": str(e)}), 500
