from app import init_app
from commands import DropTables, CreateTables
from flask_script import Manager


app = init_app()
manager = Manager(app)

manager.add_command('create_tables', CreateTables())
manager.add_command('drop_tables', DropTables())

if __name__ == '__main__':
    manager.run()
