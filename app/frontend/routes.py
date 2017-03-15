from . import frontend


@frontend.route('/')
def index():
    return 'Hello'
