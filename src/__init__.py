from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src import routes, models

from src.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.cli.command()
def init_db():
    models.init_db()

if __name__ == "__main__":
        app.run()