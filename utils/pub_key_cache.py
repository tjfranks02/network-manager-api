import requests
import os

cache = { "a": "hello" }

def get(key):
  if (key not in cache):
    cache[key] = fetchPubKey(key)

  return cache.get(key)

def set(key, value):
  cache[key] = value

def fetchPubKey(key):
  try:
    pub_key_res = requests.get(os.environ.get("AUTH_SERVICE_URL") + "/jwt/pubkey/" + key)
    pub_key_res.raise_for_status()

    return pub_key_res.json()["publicKey"]
  except requests.exceptions.HTTPError as err:
    return None