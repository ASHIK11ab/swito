import requests
import os
import sys

URL = "https://www.googleapis.com/drive/v3/files"

QUERY_STRING = {"alt":"media"}

FILE_ID = sys.argv[1]
API_KEY = sys.argv[2]


def get_config_file_contents():
  """ Reads the lines of the configuration file. """
  with open(f"./configuration.py", "r") as file:
    lines = file.readlines()
  return lines


def is_file_contents_changed(file_contents):
  """ Checks whether the fetched configuration file and the 
    available configuration files are different. """
  contents = get_config_file_contents()

  if len(file_contents) != len(contents):
    return True
  for index in range(len(file_contents)):
    if file_contents[index] != contents[index]:
      return True
  return False


def save_config_file(contents):
  """ Saves the configuration file to the file system. """
  with open(f"./configuration.py", "w") as file:
    file.writelines(contents)


def fetch_config_file(fileId, api_key):
  """ Fetches the configuration file from Google Drive. """
  file_url = f"{URL}/{fileId}?key={api_key}"
  resp = requests.get(file_url, params=QUERY_STRING)

  file_contents = resp.text

  if not os.path.exists(f"./configuration.py") \
      or is_file_contents_changed(file_contents):
    save_config_file(file_contents)

def main():
  fetch_config_file(FILE_ID, API_KEY)

if __name__ == "__main__":
  main()