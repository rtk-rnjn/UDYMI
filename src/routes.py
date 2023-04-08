from flask import flash, redirect, render_template, url_for

from src import app, bcrypt
from src.forms import LoginForm, RegistrationForm


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
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
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
    form = LoginForm()
    if form.validate_on_submit():
        if await app.db.verify_password(  # type: ignore
            username_or_email=form.email.data, password=form.password.data
        ):
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/news")
async def news():
    return render_template("news.html", title="News", posts=posts)
