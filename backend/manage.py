from api import init_app
from api.commands import DropTables, CreateTables, Initailize

from flask_script import Manager, Server
from flask_migrate import MigrateCommand

app = init_app()
manager = Manager(app)

manager.add_command('create_tables', CreateTables())
manager.add_command('drop_tables', DropTables())
manager.add_command('init', Initailize())
manager.add_command('db', MigrateCommand)
manager.add_command('run', Server(port=9000) )

@app.after_request
def allow_cors( response ):
    response.headers[ 'Access-Control-Allow-Origin' ] = '*'
    response.headers[ 'Access-Control-Allow-Headers' ] = 'Content-Type'
    return response

if __name__ == '__main__':
    manager.run()
