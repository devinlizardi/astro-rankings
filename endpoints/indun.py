from flask import Blueprint

indun_bp = Blueprint('indun', __name__)

@indun_bp.route('/indun', methods=['GET'])
def indun():
    return 'This is a blank endpoint for indun.'
