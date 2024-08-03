from flask import Flask
from dotenv import load_dotenv
import logging
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Import cache and configure it
from config import cache

# Initialize cache
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Import endpoints
from endpoints.ping import ping_bp
from endpoints.addCash import addCash_bp
from endpoints.get_ranking import get_ranking_bp
from endpoints.indun import indun_bp

# Register blueprints
app.register_blueprint(ping_bp)
app.register_blueprint(addCash_bp)
app.register_blueprint(get_ranking_bp)
app.register_blueprint(indun_bp)


@app.route('/')
def index():
    return "Welcome to the Ranking API! Available endpoints: /ping, /addCash, /getRanking, /indun"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
