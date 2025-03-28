from flask import render_template
from voteapp.controller import app


# Catch request of page_not_found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


# Catch request of internal_server_error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html"), 500
