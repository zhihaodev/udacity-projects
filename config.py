import os
import random
import string
import json

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/catalog.db'
DEBUG = True
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
ME_INFO_URL = 'https://www.googleapis.com/userinfo/v2/me'
TOKEN_INFO_URL_PREFIX = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
UPLOADED_IMAGES_DEST = 'uploads/'
IMGUR_CLIENT_ID = 'fe5387a2e465ae6'
IMGUR_UPLOAD_URL = 'https://api.imgur.com/3/image'
IMGUR_DELETE_URL = 'https://api.imgur.com/3/image/'