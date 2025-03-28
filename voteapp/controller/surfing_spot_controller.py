from flask import Flask, request, render_template, redirect, url_for, flash
from voteapp.controller import app
from werkzeug.utils import secure_filename
from voteapp.dao.competitor_dao import CompetitorDAO
from voteapp.dao.competition_dao import CompetitionDao
from voteapp.utils.session_manager import SessionManager
import os, uuid


app.config["UPLOAD_FOLDER"] = "voteapp/static/img/"
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png", "gif"}

competitor_dao = CompetitorDAO()
competition_dao = CompetitionDao()

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/competitors", methods=["GET"])
def list_competitors():
    keyword = request.args.get("search", "")
    competitors = competitor_dao.search_competitor(keyword)
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.COMPETITOR_SETUP.value
    )

    return render_template(
        "competition/surfing_spot_management.html", competitors=competitors
    )


@app.route("/competitor/add", methods=["GET", "POST"])
def add_competitor():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        image = request.files.get("image")

        image_filename = "default.png"

        if image and allowed_file(image.filename):
            ext = os.path.splitext(image.filename)[1]
            image_filename = f"{uuid.uuid4()}{ext}"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
            image.save(image_path)

        competitor_dao.add_competitor(name, description, image_filename)

        flash("New Spot added successfully!", "success")
        return redirect(url_for("list_competitors"))

    return render_template("competition/add_surfing_spot.html")


@app.route("/competitor/edit/<int:id>", methods=["GET", "POST"])
def edit_competitor(id):
    competitor = competitor_dao.get_competitor_by_id(id)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        file = request.files.get("image")

        if file and file.filename != "":
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            # file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            current_directory = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_directory)
            file.save(os.path.join(base_dir, "static", "img", filename))
            image = filename
        else:
            image = competitor.image
        competitor_dao.edit_competitor(id, name, description, image)
        flash("Spot edited successfully!", "success")
        return redirect(url_for("list_competitors", id=id))

    return render_template("competition/edit_surfing_spot.html", competitor=competitor)


@app.route("/competitor/delete/<int:id>", methods=["POST"])
def delete_competitor(id):
    competitor_dao.delete_competitor(id)
    flash("Spot deleted successfully!", "success")
    return redirect(url_for("list_competitors"))


@app.route("/competitors/pickup", methods=["GET", "POST"])
def spot_pick():
    competition_name = request.args.get("competition_name")
    keyword = request.args.get("search", "")

    competition_id = competition_dao.get_competition_id_by_name(competition_name)
    if not competition_id:
        return redirect(
            url_for(
                "spot_pick",
                competition_name=competition_name,
                error="Competition not found",
            )
        )

    competitors = competitor_dao.search_competitor(keyword)
    existing_competitor_ids = {
        comp["id"]
        for comp in competition_dao.get_competitors_by_competition(competition_id)
    }

    if request.method == "POST":
        selected_competitor_ids = request.form.getlist("selected_competitor_ids[]")
        selected_competitor_ids = [int(id) for id in selected_competitor_ids if id]

        for competitor_id in selected_competitor_ids:
            if competitor_id in existing_competitor_ids:
                competition_dao.delete_competitor_from_competition(
                    competition_id, competitor_id
                )
            else:
                competition_dao.add_competitor_to_competition(
                    competition_id, competitor_id
                )

        flash("Spot list updated successfully!", "success")
        return redirect(url_for("spot_pick", competition_name=competition_name))

    competition_status = competition_dao.get_competition_staus(competition_id)

    return render_template(
        "competition/spot_pick.html",
        competitors=competitors,
        competition_status=competition_status,
        competition_name=competition_name,
        existing_competitor_ids=existing_competitor_ids,
    )
