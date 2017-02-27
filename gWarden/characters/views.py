from flask import Blueprint, current_app

from .models import Character

mod = Blueprint("characters", __name__, url_prefix="/characters")


@mod.route("/")
def character_index():
    pass


@mod.route("/<int:cid>")
def character_profile(cid):
    c = Character.query.get_or_404(cid)
    return "{0}".format(c.name)
