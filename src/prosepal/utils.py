import secrets
import string

def random_str():
  return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(7))