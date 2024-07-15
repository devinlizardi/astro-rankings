from flask import Blueprint, request, jsonify
import pyodbc
import logging
from config.db_configs import db_configs

indun_bp = Blueprint('indun', __name__)

@indun_bp.route('/indun', methods=['GET'])
def indun():
    char_name = request.args.get('CharName')
    
    if not char_name:
        return jsonify({"error": "CharName parameter is required"}), 400
    
    try:
        conn = pyodbc.connect(db_configs['NA'])  # Assuming the connection string is same for all, or you can adjust
        cursor = conn.cursor()
        cursor.execute("EXEC RetrieveIndun @CharName = ?", char_name)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        
        return jsonify(results)
    except pyodbc.Error as e:
        logging.error(f"Error fetching Indun data: {e}")
        return jsonify({"error": str(e)}), 500
