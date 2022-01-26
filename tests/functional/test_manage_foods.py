from tests.functional.test_index import client
from tests.functional.test_auth import login
from tests.functional.__init__ import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.helperfuncs import get_tags
from werkzeug.datastructures import FileStorage
import random, string, json


def test_add_new_food(client):
  login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

  # Random data
  food_name = f"food-{''.join(random.choices(string.ascii_letters, k = 15))}"
  # Random price between 50 and 1000.
  price = random.randrange(1, 5)*random.randrange(50, 200)
  quantity = random.randrange(1, 20)
  # Randomly select a tag.
  available_tags = get_tags()
  index = random.randrange(0, len(available_tags))
  tags = [available_tags[index].name]

  # Test food image.
  with open('static/images/favicon.png', 'rb') as fp:
    file = FileStorage(fp)
    ext = file.filename.rsplit('.')[1]
    random_filename = ''.join(random.choices(string.ascii_letters, k = 10))
    file.filename = f"{random_filename}.{ext}"

    resp = client.post('/admin/foods/add', data=dict(
      name=food_name,
      price=price,
      quantity=quantity,
      image=file,
      tags=tags
    ))

    assert resp.status_code == 200
    resp_data = json.loads(resp.data.decode('utf-8'))
    assert resp_data['msg'] == 'Food added successfully'