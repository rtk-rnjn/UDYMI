from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"

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
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@admin.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/news")
async def news():
    return render_template("news.html", title="News", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
