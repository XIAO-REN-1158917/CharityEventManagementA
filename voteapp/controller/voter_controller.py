from flask import Flask, render_template, request, redirect, url_for, session, flash
from voteapp.dao.user_dao import UserDao
from voteapp.model import User
from voteapp.utils.session_manager import SessionManager
from voteapp.model.enums import Role, Status
from voteapp.controller import app

@app.route('/managing_voter/', methods=['GET', 'POST'])
def managing_voter():
    if SessionManager.get(SessionManager.USER)['role'] not in [Role.ADMIN.value, Role.SCRUTINEER.value]:
        return redirect(url_for('home'))
    search_criteria = request.form.get('search_criteria', '')
    user_dao = UserDao()
    voters = user_dao.search_voters(search_criteria)
    SessionManager.set(SessionManager.ACTIVE_PAGE, SessionManager.Page.MANAGING_VOTER.value)
    return render_template('user/managing_voter.html', voters=voters, search_criteria=search_criteria)

@app.route('/managing_voter/view/<int:voter_id>/', methods=['GET', 'POST'])
def view_voter(voter_id):
    if SessionManager.get(SessionManager.USER)['role'] not in [Role.ADMIN.value, Role.SCRUTINEER.value]:
        return redirect(url_for('home'))
    user_dao = UserDao()
    voter = user_dao.get_voter_by_id(voter_id)
    if not voter:
        return redirect(url_for('managing_voter'))
    if request.method == 'POST':
        new_status = request.form.get('new_status')
        if new_status in [Status.ACTIVE.value, Status.INACTIVE.value]:
            user_dao.set_voter_status(voter_id, new_status)
        return redirect(url_for('view_voter', voter_id=voter_id))
    SessionManager.set(SessionManager.ACTIVE_PAGE, SessionManager.Page.MANAGING_VOTER.value)
    return render_template('user/voter_profile.html', voter=voter)