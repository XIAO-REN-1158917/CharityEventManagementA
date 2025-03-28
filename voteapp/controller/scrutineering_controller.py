from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask import jsonify
from voteapp.controller import app
from voteapp.dao.competition_dao import CompetitionDao
from voteapp.dao.competitor_dao import CompetitorDAO
from voteapp.dao.scrutineering_dao import ScrutineeringDAO
from voteapp.utils.session_manager import SessionManager
from voteapp.model.competition import Competition
from flask import request
from datetime import datetime


@app.route("/daily_votes", methods=["GET"])
def daily_votes():
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.SCRUTINEERING.value
    )
    scrutineering_dao = ScrutineeringDAO()
    result = scrutineering_dao.summary_votes()
    competition = Competition(None, result[0][0], result[0][1], result[0][2], "ongoing")
    end_date = datetime.now().date()
    dates = scrutineering_dao.generate_date_range(
        competition.voting_start_date, end_date
    )

    summary_votes = []
    for date in dates:
        item = [date, ""]
        for row in result:
            if row[3] == date:
                item[1] = row[4]
                break
        summary_votes.append(item)
    summary_votes.reverse()

    return render_template(
        "/scrutineering/daily_votes.html",
        competition=competition,
        summary_votes=summary_votes,
    )


@app.route("/unusual_votes", methods=["GET", "POST"])
def unusual_votes():
    competitionDao = CompetitionDao()
    competition_list = competitionDao.ongoing_or_ended_competition()
    SessionManager.set(
        SessionManager.ACTIVE_PAGE, SessionManager.Page.SCRUTINEERING.value
    )
    if request.method == "GET":
        return render_template(
            "/scrutineering/unusual_votes.html",
            message="initial_entry",
            competition_list=competition_list,
        )
    else:
        competition_id = request.form.get("competition_id").strip()
        ip = request.form.get("ip").strip()
        scrutineering_dao = ScrutineeringDAO()
        votes = scrutineering_dao.unusual_votes(competition_id, ip)
        message = ""
        if len(votes) == 0:
            message = "no_data"

        return render_template(
            "/scrutineering/unusual_votes.html",
            message=message,
            votes=votes,
            competition_list=competition_list,
            ip=ip,
            competition_id=competition_id,
        )


@app.route("/invalidate", methods=["POST"])
def invalidate():
    data = request.get_json()
    ids = data.get("ids")
    scrutineeringDao = ScrutineeringDAO()
    scrutineeringDao.invalidate(ids)
    return jsonify({"status": "success"})


@app.route("/approving_competition", methods=["GET", "POST"])
def approving_competition():
    if request.method == "GET":
        SessionManager.set(
            SessionManager.ACTIVE_PAGE, SessionManager.Page.SCRUTINEERING.value
        )
        competitionDao = CompetitionDao()
        competition_list = competitionDao.search_competitions("ended")
        return render_template(
            "/scrutineering/approving_competition.html",
            competition_list=competition_list,
        )
    else:
        competition_id = request.form.get("competition_id")
        competitionDao = CompetitionDao()
        competitionDao.finalize_competition(competition_id)
        competition = competitionDao.get_competition_by_id(competition_id)
        flash(
            f"Competition '{competition.name}' has been approved and is now published."
        )
        return redirect("approving_competition")
