from app import init_app
from commands import DropTables, CreateTables, DropCreateTables

from flask_script import Manager


app = init_app()
manager = Manager(app)

manager.add_command('create_tables', CreateTables())
manager.add_command('drop_tables', DropTables())
manager.add_command('re', DropCreateTables())
if __name__ == '__main__':
    manager.run()