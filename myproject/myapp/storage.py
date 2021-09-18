import pyrebase
import random
import string
import os
from base64 import b64decode

storage_link = "gs://happyspace-f4b71.appspot.com"
app_id = "1:990034038970:android:218ad60be730640553f283"
firebaseConfig = {
  "apiKey": "AIzaSyAUFd9-GB2WtkbH1l6KCh5NPbyqU2l7ros",
  "authDomain": "happyspace-f4b71.firebaseapp.com",
  "projectId": "happyspace-f4b71",
  "databaseURL":"https://happyspace-f4b71-default-rtdb.firebaseio.com",
  "storageBucket": "happyspace-f4b71.appspot.com",
  "messagingSenderId": "990034038970",
  "appId":"1:990034038970:web:e2ec4a7fdb5036c453f283"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()
test_image = "wp8093375-programming-code-wallpapers.jpg"


def generate_image_random_name():
  image_random_name = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(50))
  return image_random_name


def get_image_url(image_name):
  email = "happyface_user@gmail.com"
  password = "happyface123"
  user = auth.sign_in_with_email_and_password(email, password)
  token = user['idToken']
  image_url = storage.child(image_name).get_url(token)
  if image_url:
    return image_url

def image_upload(image_name):
  image_uploaded = storage.child(image_name).put(image_name)
  if image_uploaded:
    image_url = get_image_url(image_name)
    return image_url


def decode_write_and_upload_image(image_string):
  image_name = os.getcwd() + "/" + generate_image_random_name()
  with open(image_name, "wb") as fh:
      fh.write(b64decode(image_string))
  image_url = image_upload(image_name)
  if image_url:
    return image_url