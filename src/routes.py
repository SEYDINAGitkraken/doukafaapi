from src import app
from flask_login import current_user, login_user
from src.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'user is authenticated'

@app.route('/')
def index():
    return "Hello, World!"