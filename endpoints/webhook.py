from flask import Blueprint, request, jsonify, abort
import logging
webhook_bp = Blueprint('webhook', __name__)

SECRET = "dsadasxcfe3e32ezaxdsad3aSG"

@webhook_bp.route('/webhook', methods=['GET'])
def webhook_get():
    # Extract parameters from the GET request
    secret = request.args.get('secret')
    addr = request.args.get('addr')
    status = request.args.get('status')
    order_id = request.args.get('order_id')

    # Check if the secret matches
    if secret != SECRET:
        return jsonify({'error': 'Invalid secret'}), 403

    # Return the extracted information
    return jsonify({
        'addr': addr,
        'status': status,
        'order_id': order_id
    }), 200
