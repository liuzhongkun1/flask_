from flaskScript import create_app, db
from flask_script import Manager
from flask_migrate import Migrate

app = create_app()
manage = Manager(app)
Migrate(app, db)

if __name__ == '__main__':
    manage.run()
