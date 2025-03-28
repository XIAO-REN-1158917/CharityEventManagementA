from flask import render_template, session, redirect, url_for, flash, request
from voteapp.dao.competition_dao import CompetitionDao
from voteapp.dao.vote_dao import VoteDao
from voteapp.dao.user_dao import UserDao
from voteapp.controller import app
from voteapp.utils.session_manager import SessionManager

competition_dao = CompetitionDao()
vote_dao = VoteDao()
user_dao = UserDao()


@app.route("/current_voting")
def current_voting():
    if "user_id" not in session:
        session["user_id"] = None
    if "user_role" not in session:
        session["user_role"] = None
    competitions = competition_dao.current_competition("ongoing")
    session.pop("competitor_id", None)
    SessionManager.set(SessionManager.ACTIVE_PAGE, SessionManager.Page.VOTING.value)
    return render_template("competition/current_voting.html", competitions=competitions)


@app.route("/competition/<int:competition_id>/competitor/<int:competitor_id>")
def competitor_details(competition_id, competitor_id):
    if "user_id" not in session:
        session["login_required"] = True
        return redirect(url_for("login"))
    user_role = session.get("user_role")
    if user_role != "voter":
        session["role_incorrect"] = True
        return redirect(url_for("current_voting"))
    session["competition_id"] = competition_id
    session["competitor_id"] = competitor_id
    competition_competitor, competitor = competition_dao.get_competitor_details(
        competitor_id
    )
    if not competition_competitor:
        session["competitor_not_found"] = True
        return redirect(url_for("current_voting"))
    has_voted = vote_dao.has_voted(competition_id, session["user_id"])
    SessionManager.set(SessionManager.ACTIVE_PAGE, SessionManager.Page.VOTING.value)
    return render_template(
        "competition/competitor_details.html",
        competitor=competitor,
        has_voted=has_voted,
    )


@app.route("/vote", methods=["POST"])
def vote():
    if "user_id" not in session:
        session["login_required"] = True
        return redirect(url_for("login"))
    competition_id = session.get("competition_id")
    competitor_id = session.get("competitor_id")
    voter_id = session.get("user_id")
    if not competition_id or not competitor_id or not voter_id:
        session["vote_error"] = "Voting session data is missing."
        return redirect(url_for("current_voting"))
    competition_competitor_id = competition_dao.get_competition_competitor_id(
        competition_id, competitor_id
    )
    if not competition_competitor_id:
        session["vote_error"] = "Invalid voting data."
        return redirect(url_for("current_voting"))
    success, message = vote_dao.record_vote(
        competition_competitor_id, voter_id, request.remote_addr
    )
    session["vote_result"] = message
    return redirect(
        url_for(
            "competitor_details",
            competition_id=competition_id,
            competitor_id=competitor_id,
        )
    )


@app.route("/back", methods=["POST"])
def back():
    session.pop("competitor_id", None)
    return redirect(url_for("current_voting"))
