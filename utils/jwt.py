import jwt
import utils.pub_key_cache as key_cache
import os
import requests

def verify_access_token(access_token):
  # Decode token header to get kid claim
  decoded_header = jwt.get_unverified_header(access_token)
  kid = decoded_header["kid"]

  # Get public key from cache
  pub_key = key_cache.get(kid)

  # kid not found in cache or auth service
  if not pub_key:
    return False

  # Verify access token
  try:
    decoded_token = jwt.decode(access_token, pub_key, algorithms=["RS256"])
  except Exception:
    return False

  return decoded_token