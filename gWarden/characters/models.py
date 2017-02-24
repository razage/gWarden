from datetime import datetime

from gWarden import db
from gWarden.models import BaseModel


class Character(BaseModel):
    name = db.Column(db.String(32))
    server = db.Column(db.String(32))
    level = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    race_id = db.Column(db.Integer, db.ForeignKey("races.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    spec_id = db.Column(db.Integer, db.ForeignKey("specializations.id"))
    guild_rank = db.Column(db.String(32))
    ilevel = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    race = db.relationship("Race", backref="characters_of_race", foreign_keys=race_id)
    klass = db.relationship("Class", backref="characters_of_class", foreign_keys=class_id)
    spec = db.relationship("Specialization", backref="characters_of_spec", foreign_keys=spec_id)

    def __init__(self, name, server, level, gender, guild_rank, ilevel):
        self.name = name
        self.server = server
        self.level = level
        self.gender = gender
        self.guild_rank = guild_rank
        self.ilevel = ilevel

    @property
    def role(self):
        return self.spec.role if self.spec_id is not None else "N/a"
