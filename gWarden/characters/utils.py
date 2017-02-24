import requests

from gWarden import app
from gWarden.characters.models import Character


def get_character(character):
    c = Character.query.filter(Character.name == character).first()
    if c is None:
        return
    else:
        params = {"fields": "items,guild,talents", "locale": "en_US", "apikey": app.config['SETTINGS']['api_key']}
        url = "https://us.api.battle.net/wow/character/{0}/{1}".format(c.server, character)
        r = requests.get(url, params=params)

        d = r.json()
        current_spec = None

        for specs in d['talents']:
            if 'selected' in specs:
                current_spec = specs['talents'][0]['spec']['name']

        print(current_spec)
