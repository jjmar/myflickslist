from . import auth


@auth.login('/login', methods=['POST'])
def login():
    return 'login'


@auth.route('/register', methods=['POST'])
def register():
    return 'reg'


@auth.route('/protected', methods=['POST'])
def protected():
    return 'protected'