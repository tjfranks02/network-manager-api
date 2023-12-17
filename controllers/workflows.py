from flask import request, Blueprint
import requests

import uuid

from utils.db import get_cursor, commit

import utils.pub_key_cache as cache

bp = Blueprint("workflows", __name__, url_prefix="/workflows")

@bp.post("/createdb")
def create_db():
  try:
    curr = get_cursor()

    curr.execute("""
      CREATE TABLE IF NOT EXISTS workflows (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        description VARCHAR(255)
      )
    """)

    commit()
    curr.close()

    return { "message": "Success." }, 200
  except Exception as err:
    return { "message": "Internal server error" }, 500

@bp.post("/create")
def create_workflow():
  try:
    name = request.json.get("name")
    description = request.json.get("description")

    id = uuid.uuid4()

    if (not name or not description):
      return { "message": "Missing required fields." }, 422

    curr = get_cursor()

    curr.execute("""INSERT INTO workflows (id, name, description) VALUES (%s, %s, %s)""", 
      (id, name, description)
    )

    commit()

    return { "id": id }, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    print(err)
    return { "message": "Internal server error" }, 500
  
@bp.get("/<string:workflow_id>")
def get_workflow(workflow_id):
  try:
    curr = get_cursor()

    curr.execute("""SELECT * FROM workflows WHERE id = %s""", (workflow_id,))

    workflow = curr.fetchone()

    if not workflow:
      return { "message": "Workflow not found." }, 404

    return { "workflow": workflow }, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500