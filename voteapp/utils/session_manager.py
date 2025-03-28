from flask import session
from enum import Enum


class SessionManager:
    # Session keys as constants
    USER = "user"
    ACTIVE_PAGE = "active_page"

    class Page(Enum):
        HOME = "home"
        VOTING = "current_voting"
        COMPETITION_RESULTS = "competition_results"
        LOGIN = "login"
        COMPETITION_SETUP = "competition_setup"
        COMPETITOR_SETUP = "competitor_setup"
        MANAGING_USER = "managing_user"
        SCRUTINEERING = "scrutineering"
        MANAGING_VOTER = "managing_voter"
        ANNOUNCEMENT_SETUP = "announcement_setup"
        USER_PROFILE = "user_profile"
        CHANGE_PASSWORD = "change_password"

    @staticmethod
    def set(key, value):
        """set session variable"""
        session[key] = value

    @staticmethod
    def get(key):
        """get session variable"""
        return session.get(key)

    @staticmethod
    def remove(key):
        """remove session variable"""
        if key in session:
            del session[key]

    @staticmethod
    def clear():
        """clear all session variable"""
        session.clear()
