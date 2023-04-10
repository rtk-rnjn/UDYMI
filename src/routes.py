from __future__ import annotations
import os

from flask import flash, redirect, render_template, url_for, request

from src import app, bcrypt
from src.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from src.modals import User

posts = [
    {
        "company": "Company 1",
        "title": "title of the problem statement",
        "content": "content of the problem statement",
        "date_posted": "April 5, 2023",
    },
    {
        "company": "Company 2",
        "title": "title of the problem statement",
        "content": "content of the problem statement",
        "date_posted": "April 5, 2023",
    },
]


@app.route("/")
@app.route("/home")
async def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
async def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
async def register():
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        if await app.db.register_user(  # type: ignore
            username=form.username.data, email=form.email.data, password=hashed_password
        ):
            flash(f"Account created for {form.username.data}!", "success")
        else:
            flash(f"Account already exists for {form.username.data}!", "danger")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
async def login():
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        if await app.db.verify_password(  # type: ignore
            username_or_email=form.email.data, password=form.password.data
        ):
            user = await app.db.get_user(username=form.email.data)  # type: ignore
            if user is not None:
                user = User(**user)
                if login_user(user, remember=form.remember.data):
                    next_page = request.args.get("next")
                    return (
                        redirect(next_page) if next_page else redirect(url_for("home"))
                    )
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/news")
async def news():
    return render_template("news.html", title="News", posts=posts)


@app.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
async def account():
    user: dict = await app.db.get_user_by_id(_id=current_user._id)  # type: ignore
    path = f"static/profile_pics/{user['_id']}.jpg"
    # check if path exists
    if not os.path.exists(path):
        path = "static/profile_pics/default.png"
    img = url_for("static", filename=path[7:])
    return render_template("account.html", title="Account", user=user, img=img)
