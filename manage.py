from app import init_app
from app.api.commands import DropTables, CreateTables, Initailize

from flask_script import Manager
from flask_migrate import MigrateCommand

app = init_app()
manager = Manager(app)

manager.add_command('create_tables', CreateTables())
manager.add_command('drop_tables', DropTables())
manager.add_command('init', Initailize())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
