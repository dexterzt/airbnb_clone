from flask import *
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)

from views import *
