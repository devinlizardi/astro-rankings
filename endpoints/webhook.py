from flask import Blueprint, request, jsonify, abort
import logging

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
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

        # Define possible keys to look for the custom fields
        account_name_field = next((field for field in custom_fields if field.get('key') == 'Account Name'), None)
        character_name_field = next((field for field in custom_fields if field.get('key') == 'Character Name'), None)

        # Extract the values of the custom fields if they are present
        account_name = account_name_field.get('value') if account_name_field else 'Account Name not specified'
        character_name = character_name_field.get('value') if character_name_field else 'Character Name not specified'

        return jsonify({
            'account_name': account_name,
            'character_name': character_name
        })
    
    except KeyError as e:
        logging.error(f"Key error in processing the webhook: {str(e)}")
        abort(400, f"Key error: {str(e)}")
    except TypeError as e:
        logging.error(f"Type error in processing the webhook: {str(e)}")
        abort(400, f"Type error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500, f"Unexpected server error: {str(e)}")
