from gWarden import app
from gWarden.characters.views import mod as character_mod
from gWarden.filters import remove_space

# Flask Blueprints
app.register_blueprint(character_mod)

# Jinja2 filters
app.jinja_env.filters['remove_space'] = remove_space

app.run(debug=True)
