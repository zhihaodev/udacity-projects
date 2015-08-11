"""Error handlers for different status code.
JSON response or rendered HTML will be returned.

"""

from flask import render_template, request, jsonify, make_response
from dict2xml import dict2xml as xmlify
from . import main
from ..exceptions import InvalidUsageException


@main.app_errorhandler(400)
def bad_request(e):
    """Handler for 400 bad request."""

    message = 'Bad Request'

    # JSON error response
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 400
        return response

     # XML error response
    if 'text/xml' in request.accept_mimetypes and \
            not request.accept_mimetypes.accept_html:
        response = make_response(xmlify({'error': message}, indent="  "))
        response.headers["Content-Type"] = "text/xml"
        return response

    # HTML error response
    return render_template('error/error.html', message=message), 400


@main.app_errorhandler(401)
def unauthorized(e):
    """Handler for 401 unauthorized."""

    message = 'Unauthorized'

    # JSON error response
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 401
        return response

    # XML error response
    if 'text/xml' in request.accept_mimetypes and \
            not request.accept_mimetypes.accept_html:
        response = make_response(xmlify({'error': message}, indent="  "))
        response.headers["Content-Type"] = "text/xml"
        return response

    # HTML error response
    return render_template('error/error.html', message=message), 401


@main.app_errorhandler(404)
def page_not_found(e):
    """Handler for 404 page not found."""

    message = 'Page Not Found'

    # JSON error response
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 404
        return response

    # XML error response
    if 'text/xml' in request.accept_mimetypes and \
            not request.accept_mimetypes.accept_html:
        response = make_response(xmlify({'error': message}, indent="  "))
        response.headers["Content-Type"] = "text/xml"
        return response

    # HTML error response
    return render_template('error/error.html', message=message), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Handler for 500 internal server error."""

    message = 'Internal Server Error'

    # JSON error response
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': message})
        response.status_code = 500
        return response

    # XML error response
    if 'text/xml' in request.accept_mimetypes and \
            not request.accept_mimetypes.accept_html:
        response = make_response(xmlify({'error': message}, indent="  "))
        response.headers["Content-Type"] = "text/xml"
        return response

    # HTML error response
    return render_template('error/error.html', message=message), 500


@main.app_errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    """Handler for InvalidUsageException."""

    # JSON error response
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # XML error response
    if 'text/xml' in request.accept_mimetypes and \
            not request.accept_mimetypes.accept_html:
        response = make_response(xmlify({'error': error.message}, indent="  "))
        response.headers["Content-Type"] = "text/xml"
        return response

    # HTML error response
    return render_template('error/error.html',
                           message=error.message), error.status_code
