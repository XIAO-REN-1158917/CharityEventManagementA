from flask import Flask
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.urandom(24)

from . import error_controller
from . import auth_controller
from . import home_controller
from . import competition_controller
from . import voting_controller
from . import surfing_spot_controller
from . import voter_controller
from . import management_controller
from . import user_controller
from . import scrutineering_controller
