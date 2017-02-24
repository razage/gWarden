import json
from os.path import abspath, dirname, join

BASEDIR = abspath(dirname(__file__))
SETTINGS = json.load(open(join(BASEDIR, "settings.json")))
SECRET_KEY = SETTINGS['secret_key']

if SETTINGS['db_type'] == "mysql":
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(SETTINGS['db_user'], SETTINGS['db_pass'], SETTINGS['db_host'], SETTINGS['db'])
elif SETTINGS['db_type'] == "sqlite":
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(join(BASEDIR, "database.db"))
else:
    print("Database type {0} is not currently supported.".format(SETTINGS['db_type']))

SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True

GENDERS = ("Male", "Female")
ROLES = ("Healer", "Tank", "DPS", "RDPS")
