import os

# Config file, put all your keys and passwords and whatnot in here
DB_URI = os.environ.get("DATABASE_URL", "postgres:///my_app.db")
SECRET_KEY = "this should be a secret"
