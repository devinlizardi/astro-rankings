from flask import Blueprint, request, jsonify, abort
import logging

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET'])
def webhook_get():
    # Extract parameters from the GET request
    addr = request.args.get('addr')
    status = request.args.get('status')
    order_id = request.args.get('order_id')
    
    # Return the extracted information
    return jsonify({
        'addr': addr,
        'status': status,
        'order_id': order_id
    }), 200
