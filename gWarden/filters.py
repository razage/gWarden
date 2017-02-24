from gWarden import app


@app.template_filter('remove_space')
def remove_space(string):
    return string.replace(' ', '')
