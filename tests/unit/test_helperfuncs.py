from init import create_app
import os, random, string
from utils.helperfuncs import *

app = create_app()
app.app_context().push()


def test_login_valid():
  # Test for existing user.
  username = app.config['TEST_USERNAME']
  password = app.config['TEST_PASSWORD']
  assert login_valid(username, password) == True

  # Test for failure case.
  username = 'lsdjf'
  password = 'lksdjslj'
  assert login_valid(username, password) == False


def test_username_exists():
  # Successfull case
  username = app.config['TEST_USERNAME']
  assert username_exists(username) == True

  # Failure case
  username = 'lsdjkje'
  assert username_exists(username) == False


def test_add_user():
  username = ''.join(random.choices(string.ascii_letters, k = 15))
  password = ''.join(random.choices(string.ascii_letters, k = 15))
  add_user(username, password)

  user = User.query.filter(User.username == username).first()
  # Successfull case. When user is added successfully the query
  # should return a record.
  assert not user is None


def test_valid_extension():
  valid_filenames = ['pizza.jpeg', 'donut.png', 'cake.jpg']
  for filename in valid_filenames:
    assert valid_extension(filename) == True

  invalid_filenames = ['app.py', 'index.html', 'cake.svg']
  for filename in invalid_filenames:
    assert valid_extension(filename) == False

  
def test_food_tag_exists():
  tags = Tags.query.all()
  for tag in tags:
    assert food_tag_exists(tag.name) == True

  random_tag = ''.join(random.choices(string.ascii_letters, k = 15))
  # Newly created tag will not exist until added to database.
  assert food_tag_exists(random_tag) == False


def test_create_food_tag():
  random_tag = ''.join(random.choices(string.ascii_letters, k = 15))
  create_food_tag(random_tag)
  # Tag is added and therefore should exist.
  assert food_tag_exists(random_tag) == True


def test_add_food_to_db():
  # Random data
  food_name = f"food-{''.join(random.choices(string.ascii_letters, k = 15))}"
  # Random price between 50 and 1000.
  price = random.randrange(1, 5)*random.randrange(50, 200)
  quantity = random.randrange(1, 20)
  img_url = "https://test-url"
  available_tags = get_tags()
  index = random.randrange(0, len(available_tags))
  tags = [available_tags[index].name]

  add_food_to_db(food_name, price, quantity, img_url, tags)
  
  # After adding food retrieve with its details to test whether
  # the food is added successfully.
  food_id = Food.query.with_entities(Food.id)\
            .filter(
              Food.name == food_name, Food.price == price,
              Food.quantity == quantity, Food.img_url == img_url
            ).first()[0]
  assert not food_id is None

  # Test whether foods associated tags is added successfully.
  food_tags = get_food_tags(food_id)
  assert food_tags == tags 