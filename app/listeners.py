from flask import current_app, flash, abort
from .helpers import delete_image


def receive_before_delete(mapper, connection, target):
    """Listen for the 'before_delete' event. This is to make sure
    an uploaded image is deleted from Imgur when its associated record
    is deleted from database.
    """

    if target.img_deletehash is not None:
        if not delete_image(target.img_deletehash):
            flash("Failed to delete %s." % target.name)
            abort(500)
