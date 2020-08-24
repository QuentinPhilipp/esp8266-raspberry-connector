"""
The flask application package.
"""

from flask import Flask


app = Flask(__name__)

import SensorInterfacing.routes

app.register_blueprint(SensorInterfacing.routes.main_bp)
