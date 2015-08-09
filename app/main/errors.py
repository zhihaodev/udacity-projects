"""Error handlers for different status code.
JSON response or rendered HTML will be returned.

"""

from flask import render_template, request, jsonify
from . import main
from ..exceptions import InvalidUsageException


@main.app_errorhandler(400)
def bad_request(e):
    """Handler for 400 bad request."""

    message = 'Bad Request'
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 400
        return response
    return render_template('error/error.html', message=message), 400


@main.app_errorhandler(401)
def unauthorized(e):
    """Handler for 401 unauthorized."""

    message = 'Unauthorized'
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 401
        return response
    return render_template('error/error.html', message=message), 401


@main.app_errorhandler(404)
def page_not_found(e):
    """Handler for 404 page not found."""

    message = 'Page Not Found'
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 404
        return response
    return render_template('error/error.html', message=message), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Handler for 500 internal server error."""

    message = 'Internal Server Error'
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 500
        return response
    return render_template('error/error.html', message=message), 500


@main.app_errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    """Handler for InvalidUsageException."""

    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    return render_template('error/error.html',
                           message=error.message), error.status_code
