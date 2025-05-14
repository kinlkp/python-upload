import os

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd1234'
bootstrap = Bootstrap(app)

runtime_env = os.getenv('FLASK_RUNTIME_ENV')


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

database_dir = f"{os.path.abspath(os.path.dirname(__file__))}/../db/"
database_uri = f'sqlite:///{database_dir}/{runtime_env}.sqlite3'

Session = sessionmaker()

engine = create_engine(database_uri)
session = Session(bind=engine)
Base.metadata.create_all(engine)