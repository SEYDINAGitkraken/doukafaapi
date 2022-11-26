from src import login

from src.flaskModels.usersModel import User, UserRoles
from src.flaskModels.categoryModel import Category
from src.flaskModels.platsModel import Plat

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


