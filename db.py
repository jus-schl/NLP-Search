from app import app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
print(getenv("DATABASE_URL"))
db = SQLAlchemy(app)