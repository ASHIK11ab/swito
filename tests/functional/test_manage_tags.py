from tests.functional.test_index import client
from tests.functional.test_auth import login
from tests.functional.__init__ import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.helperfuncs import get_tags
import random, string, json


def test_add_tag(client):
  login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

  random_tag = ''.join(random.choices(string.ascii_letters, k = 15))
  resp = client.post('/admin/foods/tags/add', data=dict(name=random_tag))

  assert resp.status_code == 200
  resp_data = json.loads(resp.data.decode('utf-8'))
  assert resp_data['msg'] == "Tag created successfully"

  tags = get_tags()
  tag_name = tags[0].name
  resp = client.post('/admin/foods/tags/add', data=dict(name=tag_name))
  
  # Available tag name when added should return error.
  assert resp.status_code == 404
  resp_data = json.loads(resp.data.decode('utf-8'))
  assert resp_data['msg'] == "Tag name not available"