import requests
import os
import sys

URL = "https://www.googleapis.com/drive/v3/files"

QUERY_STRING = {"alt":"media"}

FILE_ID = sys.argv[1]
API_KEY = sys.argv[2]


def get_creds_file_contents():
  """ Reads the lines of the credential file. """
  with open(f"./swito-google-creds.json", "r") as file:
    lines = file.readlines()
  return lines


def save_creds_file(contents):
  """ Saves the credential file to the file system. """
  with open(f"./swito-google-creds.json", "w") as file:
    file.writelines(contents)


def fetch_creds_file(fileId, api_key):
  """ Fetches the credential file from Google Drive. """
  file_url = f"{URL}/{fileId}?key={api_key}"
  resp = requests.get(file_url, params=QUERY_STRING)

  file_contents = resp.text

  save_creds_file(file_contents)

def main():
  fetch_creds_file(FILE_ID, API_KEY)

if __name__ == "__main__":
  main()