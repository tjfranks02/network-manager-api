import psycopg2
import os

os.environ.get("AUTH_SERVICE_URL")

conn = psycopg2.connect(
  database = os.environ.get("POSTGRES_DB"), 
  user = os.environ.get("POSTGRES_USER"), 
  host= os.environ.get("POSTGRES_HOST"),
  password = os.environ.get("POSTGRES_PASSWORD"),
  port = os.environ.get("POSTGRES_PORT")
)

def get_cursor():
  return conn.cursor()

def commit():
  conn.commit()