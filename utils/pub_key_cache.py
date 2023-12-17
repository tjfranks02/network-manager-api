import requests
import os

# KVM from kid->public key
cache = {}

def get(kid):
  """
  Get the public key corresponding to kid from the cache. If it doesn't exist, fetch it from the
  auth service and cache it if it exists.

  Params:
    kid (string): The kid claim of the JWT assigned by the auth service.

  Returns:
    string: The public key corresponding to the kid claim. None if the kid doens't exist in the
    cache or auth service.
  """
  if cache.get(kid):
    return cache.get(kid)
  
  pub_key = fetch_pub_key(kid)

  if pub_key:
    set(kid, pub_key)

  return pub_key

def set(kid, pubKey):
  """
  Set the public key corresponding to kid in the cache.
  """
  cache[kid] = pubKey

def fetch_pub_key(key):
  """
  Fetch the public key corresponding to kid from the auth service. If it doesn't exist, return None.

  Params:
    key (string): The kid claim of the JWT assigned by the auth service.

  Returns:
    string: The public key corresponding to the kid claim. None if the kid doesn't exist in the
    auth service.
  """
  try:
    pub_key_res = requests.get(os.environ.get("AUTH_SERVICE_URL") + "/jwt/pubkey/" + key)
    pub_key_res.raise_for_status()

    return pub_key_res.json()["publicKey"]
  except requests.exceptions.HTTPError as err:
    return None