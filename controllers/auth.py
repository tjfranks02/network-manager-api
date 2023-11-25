from flask import request, make_response, Blueprint
import requests
import os

from utils.auth import attach_cookie_to_res

bp = Blueprint("auth", __name__, url_prefix="/users")

@bp.post("/signin")
def signIn():
  # Forward the request to the auth service
  try:
    sign_in_res = requests.post(
      os.environ.get("AUTH_SERVICE_URL") + "/users/signin",
      json=request.json
    )
    sign_in_res.raise_for_status()

    res = make_response({ "message": "Success." })

    attach_cookie_to_res(res, "accessToken", sign_in_res.json()["accessToken"])
    attach_cookie_to_res(res, "refreshToken", sign_in_res.json()["refreshToken"])
    return res, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500
  
@bp.post("/signup")
def signUp():
  # Forward request to the auth microservice
  try:
    # Forward the request to the auth service
    sign_in_res = requests.post(
      os.environ.get("AUTH_SERVICE_URL") + "/users/signup",
      json=request.json
    )

    sign_in_res.raise_for_status()

    res = make_response({ "message": "Success." })

    attach_cookie_to_res(res, "accessToken", sign_in_res.json()["accessToken"])
    attach_cookie_to_res(res, "refreshToken", sign_in_res.json()["refreshToken"])
    return res, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500