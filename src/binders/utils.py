import secrets
import string
import json
import os

import chardet
import requests


def is_encoding(file_path: str, encoding: str) -> bool:
  try:
    with open(file_path, "r", encoding=encoding) as f:
      f.read()
    return True
  except UnicodeDecodeError:
    return False

def auto_detect_encoding(file_path: str) -> str:
  with open(file_path, 'rb') as f:
    raw_data = f.read()
  return chardet.detect(raw_data)['encoding']

def manual_detect_encoding(file_path: str) -> str:
  for encoding in ["iso-8859-1", "windows-1252", "utf-16", "utf-32", "iso-8859-2", "iso-8859-5", "iso-8859-6", "iso-8859-7", "iso-8859-9"]:
    if is_encoding(file_path, encoding):
      return encoding
  return ""

def recode_text(original_file_path: str) -> str:
  base_name, ext = os.path.splitext(original_file_path)
  recoded_file_path = f"{base_name}-recoded{ext}"
  detected_encoding = auto_detect_encoding(original_file_path) or manual_detect_encoding(original_file_path)
  with open(original_file_path, "r", encoding=detected_encoding or "utf-8", errors="ignore") as f:
    content = f.read()
  with open(recoded_file_path, "w", encoding="utf-8") as f:
    f.write(content)

def read_text_file(file_path: str) -> str:
  with open(file_path, "r") as f:
    read_file = f.read()
  return read_file

def write_to_file(content: str, file: str):
  with open(file, "w") as f:
    f.write(content)

def write_jsonl_file(content: str, file_path: str):
  with open(file_path, "a") as f:
    for item in content:
      json.dump(item, f)
      f.write("\n")
  return

def random_str():
  return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(7))

def check_pdf_in_storage(pdf_path):
  pass

def process_lorebinder(data, user):
  pass

def contact(email, name, message):
  pass

def check_email(user_email: str) -> bool:
  api_key =  os.environ.get("abstract_api_key")
  url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={user_email}"
  response = requests.get(url).json()
  if response.get("deliverability") != "DELIVERABLE":
    return False
  if not response.get("is_valid_format", {}).get("value"):
    return False
  if not response.get("is_smtp_valid", {}).get("value"):
    return False
  return True