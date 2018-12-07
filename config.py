class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/todoapp.db '
    SQLALCHEMY_TRACK_MODIFICATIONS = False