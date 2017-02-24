from gWarden import app, db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class APIMap(BaseModel):
    __abstract__ = True
    name = db.Column(db.String(20))
    blizz_id = db.Column(db.Integer)

    def __init__(self, name, blizz_id):
        self.name = name
        self.blizz_id = blizz_id


class Race(APIMap):
    __tablename__ = "races"


class Class(APIMap):
    __tablename__ = "classes"


class Specialization(BaseModel):
    __tablename__ = "specializations"
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    name = db.Column(db.String(20))
    role = db.Column(db.String(6))

    klass = db.relationship("Class", backref="specs", foreign_keys=class_id)

    def __init__(self, name, role):
        self.name = name

        if role in app.config['ROLES']:
            self.role = role
        else:
            self.role = "DPS"
