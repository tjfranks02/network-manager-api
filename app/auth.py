import os
from flask import Blueprint, request
import requests

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/signin", methods=["POST"])
def signIn():
  print(request.json)

  # Forward the request to the auth service
  sign_in_res = requests.post(
    os.environ.get("AUTH_SERVICE_URL") + "/users/signin",
    json=request.json
  )

  return sign_in_res.content, sign_in_res.status_code, sign_in_res.headers.items()