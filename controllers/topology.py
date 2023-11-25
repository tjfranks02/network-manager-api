from flask import request, Blueprint
import requests

import utils.jwt as jwtUtils

bp = Blueprint("topology", __name__, url_prefix="/topology")

@bp.before_request
def beforeRequest():
  # Check if the request is authorized
  try:
    # Get the access token from the request cookies
    access_token = request.cookies.get("accessToken")
    jwtUtils.verify_access_token(access_token)
  except Exception:
    return { "message": "You must be signed in." }, 401

@bp.get("/<int:topology_id>")
def getTopology(topology_id):
  try:
    # TODO: Fetch the topology from database
    return { "message": "Success." }, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500