"""Helper functions for utilizing imgur api service."""
import requests
from base64 import b64encode

ClIENT_ID = 'fe5387a2e465ae6'
IMGUR_UPLOAD_URL = 'https://api.imgur.com/3/image'
IMGUR_DELETE_URL = 'https://api.imgur.com/3/image/'


def upload_image(stream):
    """Upload an image to Imgur.

    Args:
        stream: image stream
    """

    data = {
        'image': b64encode(stream.read()),
        'type': 'base64'
    }
    headers = {'Authorization': 'Client-ID ' + ClIENT_ID}
    r = requests.post(IMGUR_UPLOAD_URL, data=data, headers=headers)
    # print r.json()
    if r.status_code != requests.codes.ok:
        return None, None
    return r.json()['data']['link'], r.json()['data']['deletehash']


def delete_image(deletehash):
    """Delete an image on Imgur by its deletehash.

    Args:
        deletehash: image's deletehash
    """
    
    headers = {'Authorization': 'Client-ID ' + ClIENT_ID}
    r = requests.delete(IMGUR_DELETE_URL + deletehash, headers=headers)
    # print r.json()
    return r.status_code == requests.codes.ok
