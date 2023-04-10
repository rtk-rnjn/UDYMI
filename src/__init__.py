from __future__ import annotations

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.utils import CONFIG, DB
import jinja2
import asyncio
import os

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = Flask("main")

app.static_url_path = "/src/static"
app.static_folder = app.root_path + app.static_url_path

app.config["SECRET_KEY"] = CONFIG.FLASK_SECRET_KEY
app.config.from_prefixed_env("FLASK_")

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # type: ignore
login_manager.login_message_category = "info"  # type: ignore

setattr(app, "db", DB(flask_app=app, mongo_uri=CONFIG.MONGO_URI, bcrypt=bcrypt))


template_loader = jinja2.ChoiceLoader(
    [
        app.jinja_loader,  # type: ignore
        jinja2.FileSystemLoader(["src/templates", "src/templates/emails"]),
        jinja2.FileSystemLoader(["src/static"]),
    ]
)
app.jinja_loader = template_loader  # type: ignore


from src import routes
from src.modals import *
