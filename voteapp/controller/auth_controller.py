from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from voteapp.controller import app
from voteapp.dao.user_dao import UserDao
from voteapp.model import User
from datetime import datetime
from voteapp.utils.hash_utils import get_password_hash
from voteapp.model import enums
from voteapp.utils.session_manager import SessionManager


@app.before_request
def before_request():
    exempt_routes = [
        "/home/",
        "/login/",
        "/register/",
        "/instant_message/",
        "/static/",
        "/current_voting",
        "/competition_results",
        "/favicon.ico",
    ]
    if request.path == "/":
        return redirect(url_for("home"))

    if not any(request.path.startswith(route) for route in exempt_routes):
        if SessionManager.USER not in session:
            # session["next_url"] = request.path  # Save the current path to next_url
            return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        login_username = ""
        if "login_username" in session:
            login_username = session["login_username"]

        login_password = ""
        if "login_password" in session:
            login_password = session["login_password"]

        SessionManager.set(SessionManager.ACTIVE_PAGE, SessionManager.Page.LOGIN.value)
        return render_template(
            "auth/login.html",
            login_username=login_username,
            login_password=login_password,
        )
    else:
        login_username = request.form.get("login_username")
        login_password = request.form.get("login_password")
        session["login_username"] = login_username
        session["login_password"] = login_password

        user_dao = UserDao()
        result, message = user_dao.authenticate_user(login_username, login_password)

        if result == None:
            flash(message)
            return redirect(url_for("login"))
        else:
            SessionManager.set(SessionManager.USER, result.to_dict())
            session["user_role"] = result.role.value
            session["user_id"] = result.id
            return redirect(url_for("home"))
            # Retrieve the next URL to redirect to and default to home if no URL is stored
            # next_url = session.pop("next_url", url_for("home"))
            # return redirect(next_url)


@app.route("/logout/", methods=["GET"])
def logout():
    session.pop(SessionManager.USER, None)
    session.pop("login_username", None)
    session.pop("login_password", None)
    session.pop("user_role", None)
    return redirect(url_for("login"))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template(
            "auth/register.html",
            currentdate=datetime.now().date(),
        )
    else:
        reg_user_name = request.form.get("reg_user_name")
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        reg_password = request.form.get("reg_password")
        descripti = request.form.get("description") or ""
        location = request.form.get("location")
        avatar = request.form.get("avatar")
        if not avatar:
            avatar = "default.png"
        user_dao = UserDao()

        # Check if the email already exists
        existing_user = user_dao.find_by_email(email)
        if existing_user:
            flash("Email already exists. Please use a different email.")
            return render_template(
                "auth/register.html",
                currentdate=datetime.now().date(),
                reg_user_name=reg_user_name,
                email=email,
                firstname=firstname,
                lastname=lastname,
                reg_password=reg_password,
                confirm_password=reg_password,
                descripti=descripti,
                location=location,
            )

        user = User(
            None,
            reg_user_name,
            get_password_hash(reg_password),
            email,
            firstname,
            lastname,
            descripti,
            location,
            avatar,
            enums.Role.VOTER,
            enums.Status.ACTIVE,
        )

        flag, message = user_dao.register(user)
        if flag:
            flash(message)
            return redirect(url_for("login"))
        else:
            flash(message)
            return render_template(
                "auth/register.html",
                currentdate=datetime.now().date(),
                reg_user_name=reg_user_name,
                email=email,
                firstname=firstname,
                lastname=lastname,
                reg_password=reg_password,
                confirm_password=reg_password,
                descripti=descripti,
                location=location,
            )
