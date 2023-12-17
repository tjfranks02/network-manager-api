from flask import request, make_response, Blueprint
import requests
import os

import utils.pub_key_cache as cache

bp = Blueprint("topology", __name__, url_prefix="/topology")

@bp.before_request
def beforeRequest():
  cache.set("woot", "woot")
  # Check if the request is authorized
  try:
    auth_res = requests.get(
      os.environ.get("AUTH_SERVICE_URL") + "/users/authorize",
      headers = {
        "Authorization": request.headers["Authorization"]
      }
    )

    auth_res.raise_for_status()
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500

@bp.get("/<int:topology_id>")
def getTopology(topology_id):
  try:
    topology_res = requests.get(
      os.environ.get("TOPOLOGY_SERVICE_URL") + "/topology/" + str(topology_id),
      headers = {
        "Authorization": request.headers["Authorization"]
      }
    )

    topology_res.raise_for_status()

    return topology_res.json(), 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500