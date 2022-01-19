from init import create_app
from werkzeug.datastructures import FileStorage
from utils.gdriveupload import upload_file
import requests, random, string

app = create_app()
app.app_context().push()

def test_upload_file():
  with open('static/images/favicon.png', 'rb') as fp:
    file = FileStorage(fp)
    ext = file.filename.rsplit('.')[1]
    random_filename = ''.join(random.choices(string.ascii_letters, k = 10))
    file.filename = f"{random_filename}.{ext}"

    # For testing use upload image to foods directory in gdrive.
    status, img_url = upload_file(file, "FOODS")
    res = requests.get(img_url)
    assert res.status_code == 200