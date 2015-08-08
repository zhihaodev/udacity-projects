from flask import current_app, flash, abort
from .helpers import delete_image


def receive_before_delete(mapper, connection, target):
    "listen for the 'after_delete' event"

    print "Deleting item..." + target.name

    if target.img_deletehash is not None:
        if not delete_image(target.img_deletehash):
            flash("Failed to delete %s." % target.name)
            abort(501)
