from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user


@app.route("/user/home")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    return render_template(
        "pages/dashboard.html",
        current_user=user.User.getById({"id": session["user_id"]}),
    )

    # need to pass info for garden and tasks via class methods if we are rendering anything for them here - same for garden create, task create
