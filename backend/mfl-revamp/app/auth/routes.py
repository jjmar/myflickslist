from . import auth

@auth.route('/register')
def register():
    return 'reg'