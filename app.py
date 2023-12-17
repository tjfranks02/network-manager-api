from flask import Flask
from flask_cors import CORS
import dotenv
import psycopg2.extras

# Allows working with uuid type
psycopg2.extras.register_uuid()

# Routes blueprints
from controllers import auth, topology, workflows

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r'/*': { "origins": ["http://localhost:5173"]} })

app.register_blueprint(auth.bp)
app.register_blueprint(topology.bp)
app.register_blueprint(workflows.bp)