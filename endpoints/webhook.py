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
