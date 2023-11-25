def attach_cookie_to_res(res, name, value):
  res.set_cookie(name, value, httponly = True)