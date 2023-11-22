from flask import Flask, request, make_response
import requests
import os
from flask_cors import CORS
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r'/*': { "origins": ["http://localhost:5173"]} })

@app.route("/")
def hello():
  return "Hello, World!"

@app.post("/signin")
def signIn():
  # Forward the request to the auth service
  try:
    sign_in_res = requests.post(
      os.environ.get("AUTH_SERVICE_URL") + "/users/signin",
      json=request.json
    )

    sign_in_res.raise_for_status()

    res = make_response({ "message": "Success." })
    res.set_cookie("accessToken", sign_in_res.json()["accessToken"], httponly = True)
    res.set_cookie("refreshToken", sign_in_res.json()["refreshToken"], httponly = True)
    return res, 200
  except requests.exceptions.HTTPError as err:
    return err.response.json(), err.response.status_code
  except Exception as err:
    return { "message": "Internal server error" }, 500