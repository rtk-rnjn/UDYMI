from __future__ import annotations

from flask import Flask
from flask_bcrypt import Bcrypt
from src.utils import CONFIG, DB
import jinja2

app = Flask("main")
app.config.from_prefixed_env("FLASK_")
bcrypt = Bcrypt(app)
setattr(app, "db", DB(flask_app=app, mongo_uri=CONFIG.MONGO_URI, bcrypt=bcrypt))


template_loader = jinja2.ChoiceLoader(
    [
        app.jinja_loader, # type: ignore
        jinja2.FileSystemLoader(["src/templates", "src/templates/emails"]),
        jinja2.FileSystemLoader(["src/static"])
    ]
)
app.jinja_loader = template_loader # type: ignore


from src import routes
