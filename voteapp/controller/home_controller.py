from flask import Flask
from flask import render_template
from datetime import datetime
import platform

from voteapp.controller import app
from voteapp.dao.competition_dao import CompetitionDao
from voteapp.utils.session_manager import SessionManager


def format_date(date_str):
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")

    # Format day with suffix
    day = date_obj.day
    suffix = (
        "th" if 11 <= day <= 13 else {
            1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    )

    # Format the final date string
    if platform.system() == "Windows":
        return f"{day}{suffix} {date_obj:%b %Y}"
    else:
        return date_obj.strftime(f"%-d{suffix} %b %Y")


@app.route("/instant_message/", methods=["GET"])
def instant_message():
    return render_template("index.html")


@app.route("/home/", methods=["GET"])
def home():
    SessionManager.set(SessionManager.ACTIVE_PAGE,
                       SessionManager.Page.HOME.value)

    competition_dao = CompetitionDao()

    latest_game_id, latest_game_name = competition_dao.latest_competition()
    champion_name, champion_image, vote_count = None, None, None

    if latest_game_id:
        champion_name, champion_image, vote_count = (
            competition_dao.champ_in_competition(latest_game_id)
        )

    ongoing_competition_name = None
    ongoing_voting_start_date = None
    ongoing_voting_end_date = None
    ongoing_voting_end_date_2 = None

    for competition in competition_dao.ongoing_or_ended_competition():
        if competition["competition_status"] == "ongoing":
            ongoing_competition_name = competition["competition_name"]
            ongoing_voting_start_date = format_date(
                competition["voting_start_date"])
            ongoing_voting_end_date = format_date(
                competition["voting_end_date"])
            ongoing_voting_end_date_2 = competition["voting_end_date"]

            break

    return render_template(
        "home.html",
        champion_name=champion_name,
        champion_image=champion_image,
        vote_count=vote_count,
        latest_game_name=latest_game_name,
        ongoing_competition_name=ongoing_competition_name,
        ongoing_voting_start_date=ongoing_voting_start_date,
        ongoing_voting_end_date=ongoing_voting_end_date,
        ongoing_voting_end_date_2=ongoing_voting_end_date_2,
    )
