from __future__ import annotations

from flask import Flask
from src.utils import CONFIG, DB

app = Flask(__name__)
app.config["SECRET_KEY"] = CONFIG.SECRET_KEY

setattr(app, "db", DB(flask_app=app, mongo_uri=CONFIG.MONGO_URI))

from src import routes
