from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask import jsonify
from voteapp.controller import app
from voteapp.dao.competition_dao import CompetitionDao
from voteapp.dao.competitor_dao import CompetitorDAO
from voteapp.utils.session_manager import SessionManager
from flask import request
from datetime import datetime


@app.route("/competition_results", methods=["GET"])
def competition_results():
    # Create an instance of the CompetitionDao
    competition_dao = CompetitionDao()
    # Retrieve the finalized competition results
    results = competition_dao.all_finalized_competition_results()
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.COMPETITION_RESULTS.value
    )
    # Render the home template with the competition results
    return render_template(
        "competition/competition_results.html", competition_results=results
    )


@app.route("/competition_details/<int:competition_id>", methods=["GET"])
def competition_details(competition_id):
    if "user_id" not in session:
        # store the intended URL for after login
        #session["next_url"] = url_for(
         #   "competition_details", competition_id=competition_id
        #)
        return redirect(url_for("login"))

    competition_dao = CompetitionDao()
    details = competition_dao.competition_details(competition_id)
    competition_name = competition_dao.competition_name(
        competition_id
    )  # fetch the competition name
    return render_template(
        "competition/competition_details.html",
        competition_details=details,
        competition_name=competition_name,
    )


@app.route("/competition_setup", methods=["GET", "POST"])
def competition_setup():
    competition_dao = CompetitionDao()

    # Check and update competition statuses
    competition_dao.update_status_for_expired_competitions()

    if request.method == "GET":
        SessionManager.set(
            SessionManager.ACTIVE_PAGE, SessionManager.Page.COMPETITION_SETUP.value
        )

        return render_template(
            "competition/competition_setup.html",
            message="initial_entry",
            status="all",
        )
    else:
        status = request.form.get("status")
        competition_dao = CompetitionDao()
        competition_list = competition_dao.search_competitions(status)

        message = ""
        if len(competition_list) == 0:
            message = "no_data"

        return render_template(
            "competition/competition_setup.html",
            message=message,
            competition_list=competition_list,
            status=status,
        )


@app.route("/competition_add", methods=["GET", "POST"])
def competition_add():
    if request.method == "GET":
        SessionManager.set(
            SessionManager.ACTIVE_PAGE, SessionManager.Page.COMPETITION_SETUP.value
        )
        return render_template(
            "competition/competition_add.html",
            current_date=datetime.now().date(),
            flag="add",
        )
    else:
        name = request.form.get("name")
        voting_start_date = request.form.get("voting_start_date")
        voting_end_date = request.form.get("voting_end_date")

        competition_dao = CompetitionDao()
        competition_dao.add_competition(name, voting_start_date, voting_end_date)

        flash("Competition added successfully")
        return redirect(url_for("competition_setup"))


@app.route("/competition_delete", methods=["POST"])
def competition_delete():
    id = request.form.get("id")
    competition_dao = CompetitionDao()
    competition_dao.del_competition(id)
    return jsonify({"status": "success"})


@app.route("/competition_edit", methods=["GET", "POST"])
def competition_edit():
    if request.method == "GET":
        id = request.args.get("id")
        competition_dao = CompetitionDao()
        competition = competition_dao.get_competition_by_id(id)
        SessionManager.set(
            SessionManager.ACTIVE_PAGE, SessionManager.Page.COMPETITION_SETUP.value
        )
        return render_template(
            "competition/competition_add.html",
            current_date=datetime.now().date(),
            flag="edit",
            competition=competition,
        )
    else:
        id = request.form.get("id")
        name = request.form.get("name")
        voting_start_date = request.form.get("voting_start_date")
        voting_end_date = request.form.get("voting_end_date")

        competition_dao = CompetitionDao()
        competition_dao.edit_competition(id, name, voting_start_date, voting_end_date)

        flash("Competition edited successfully")
        return redirect(url_for("competition_setup"))


@app.route("/competition_launch", methods=["POST"])
def competition_launch():
    id = request.form.get("id")
    competition_dao = CompetitionDao()
    flag, message = competition_dao.launch_competition(id)
    if flag:
        return jsonify({"message": message, "status": "success"}), 200
    else:
        return jsonify({"message": message, "status": "error"}), 400
