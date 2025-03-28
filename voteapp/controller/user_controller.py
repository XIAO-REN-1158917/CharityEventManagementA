from flask import request, render_template, redirect, url_for, flash, session
from voteapp.controller import app
from voteapp.dao.user_dao import UserDao
from voteapp.model import User
from werkzeug.utils import secure_filename
from voteapp.utils.hash_utils import get_password_hash, check_password_hash
from voteapp.utils.session_manager import SessionManager
import os


# Configure the file upload folder
app.config["UPLOAD_FOLDER"] = "voteapp/static/img/"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/profile/", methods=["GET", "POST"])
def profile():
    user_id = session["user_id"]
    user_dao = UserDao()
    user = user_dao.find_by_id(user_id)
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.USER_PROFILE.value
    )
    return render_template("user/profile.html", user=user)


@app.route("/update_profile/", methods=["GET", "POST"])
def update_profile():
    user_id = session["user_id"]
    user_dao = UserDao()
    user = user_dao.find_by_id(user_id)

    if request.method == "POST":
        # Handle profile image update
        if "profile_image" in request.files:
            file = request.files["profile_image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                # Replace old image with new one
                user.avatar = filename

                user = User.from_dict(SessionManager.get(SessionManager.USER))
                user.avatar = filename
                SessionManager.set(SessionManager.USER, user.to_dict())

                user_dao.update_user(user)
                flash("Profile image updated successfully!")
                return redirect(url_for("update_profile"))

        # Handle profile details update
        updated_email = request.form.get("email")
        updated_first_name = request.form.get("first_name")
        updated_last_name = request.form.get("last_name")
        updated_location = request.form.get("location")
        updated_description = request.form.get("description")

        if updated_email:
            # Check if the new email is unique
            existing_user = user_dao.find_by_email(updated_email)
            if existing_user and existing_user.id != user_id:
                flash("Email already exists. Please use a different email.")
            else:
                # Update user details
                user.email = updated_email
                user.first_name = updated_first_name
                user.last_name = updated_last_name
                user.location = updated_location
                user.description = updated_description

                user_dao.update_user(user)
                flash("Profile updated successfully!")
        return redirect(url_for("update_profile"))

    return render_template("user/update_profile.html", user=user)


@app.route("/delete_profile_image/", methods=["POST"])
def delete_profile_image():
    user_id = session["user_id"]
    user_dao = UserDao()
    user = user_dao.find_by_id(user_id)

    # Reset avatar to default
    user.avatar = "default.png"
    user_dao.update_user(user)
    flash("Profile image deleted successfully!")
    return redirect(url_for("profile"))


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.CHANGE_PASSWORD.value
    )
    user_id = session["user_id"]
    user_dao = UserDao()
    user = user_dao.find_by_id(user_id)
    current_password = ""
    new_password = ""
    confirm_password = ""

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check if the current password is correct
        if not check_password_hash(user.password_hash, current_password):
            flash("Current password is incorrect.")
        # Check if the new password is the same as the current password
        elif check_password_hash(user.password_hash, new_password):
            flash("New password cannot be the same as the current password.")
        # Check if the new password and confirmation match
        elif new_password != confirm_password:
            flash("New passwords do not match.")
        else:
            # Update the password in the database
            hashed_password = get_password_hash(new_password)
            user.password_hash = hashed_password
            user_dao.update_user(user)
            flash("Password changed successfully!")
            return redirect(url_for("change_password"))

    return render_template(
        "user/change_password.html",
        current_password=current_password,
        new_password=new_password,
        confirm_password=confirm_password,
    )

