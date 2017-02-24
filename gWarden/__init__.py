from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

assets = Environment(app)
assets.url = app.static_url_path

scss = Bundle("scss/main.scss", filters='pyscss', output="css/compiled.css")

assets.register('css_all', scss)


@app.route("/")
def home():
    from gWarden.characters.models import Character
    from gWarden.models import Specialization

    counts = {
        "tanks": Character.query.filter(Character.spec.has(Specialization.role == "Tank")).count(),
        "dps": Character.query.filter(Character.spec.has(Specialization.role == "DPS")).count(),
        "ranged": Character.query.filter(Character.spec.has(Specialization.role == "RDPS")).count(),
        "healers": Character.query.filter(Character.spec.has(Specialization.role == "Healer")).count(),
        "total": len(Character.query.all()),
        "avg_ilevel": db.session.query(func.avg(Character.ilevel)).filter(Character.level == 110).scalar(),
        "min_ilevel": db.session.query(func.min(Character.ilevel)).filter(Character.level == 110).scalar(),
        "max_ilevel": db.session.query(func.max(Character.ilevel)).filter(Character.level == 110).scalar()
    }

    return render_template("index.html", title="Home", roster=Character.query.order_by(Character.name).all(), counts=counts)


# TODO: this function is awful and it isn't in a good place. it should be rewritten and moved.
@app.route("/get_roster")
def get_roster():
    from gWarden.models import Class, Race, Specialization
    from gWarden.characters.models import Character

    params = {"fields": "members", "locale": "en_US", "apikey": app.config['SETTINGS']['api_key']}
    url = "https://us.api.battle.net/wow/guild/{0}/{1}".format(app.config['SETTINGS']['server'], app.config['SETTINGS']['guild'])
    r = requests.get(url, params=params)

    if r.status_code == 200:
        raw_data = r.json()

        for raw in raw_data['members']:
            if Character.query.filter(Character.name == raw['character']['name']).count() > 0:
                print("Skipping {0}".format(raw['character']['name']))
                continue
            grank = app.config['SETTINGS']['guild_ranks'][str(raw['rank'])]
            klass = Class.query.filter(Class.blizz_id == raw['character']['class']).one()
            race = Race.query.filter(Race.blizz_id == raw['character']['race']).one()
            gender = app.config['GENDERS'][raw['character']['gender']]

            _char = Character(raw['character']['name'], raw['character']['realm'], raw['character']['level'], gender, grank, 0)
            _char.klass = klass
            _char.race = race
            if 'spec' in raw['character']:
                _char.spec = Specialization.query.filter(Specialization.name == raw['character']['spec']['name'], Specialization.class_id == klass.id).one()

            params2 = {"fields": "items,guild,talents", "locale": "en_US", "apikey": app.config['SETTINGS']['api_key']}
            url2 = "https://us.api.battle.net/wow/character/{0}/{1}".format(_char.server, _char.name)
            r2 = requests.get(url2, params=params2)
            chardata = r2.json()

            _char.ilevel = chardata['items']['averageItemLevel']

            db.session.add(_char)

        db.session.commit()

    return "Nothing"

from gWarden.filters import remove_space

app.jinja_env.filters['remove_space'] = remove_space
