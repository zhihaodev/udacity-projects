from flask import render_template, request, jsonify
from . import main
from ..exceptions import InvalidUsageException


@main.app_errorhandler(400)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Bad Request'})
        response.status_code = 400
        return response
    return render_template('error/404.html'), 400


@main.app_errorhandler(401)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Unauthorized'})
        response.status_code = 401
        return response
    return render_template('error/404.html'), 401


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Page Not Found'})
        response.status_code = 404
        return response
    return render_template('error/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Internal Server Error'})
        response.status_code = 500
        return response
    return render_template('error/500.html'), 500


@main.app_errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    return render_template('error/error.html', message=error.message), error.status_code
