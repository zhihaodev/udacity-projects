"""View functions for authorization.

Reference: https://github.com/udacity/ud330/blob/master/Lesson2/step6/project.py

"""

from flask import render_template, session, request, current_app, \
    make_response, redirect, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .. import db
from ..exceptions import InvalidUsageException
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import random
import string


@auth.route('/login')
def login():
    """Render login page for logging user in."""

    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state

    # Record where user should be redirected after logging in
    next = request.args.get('next')
    if next is not None:
        session['next'] = next

    return render_template('auth/login.html', state=state,
                           client_id=current_app.config['CLIENT_ID'],
                           next=next)


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    """Logging user in by a Google+ sign-in."""

    # Validate state token
    if request.args.get('state') != session['state']:
        raise InvalidUsageException('Invalid state parameter', 401)

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        raise InvalidUsageException(
            'Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ((current_app.config['TOKEN_INFO_URL_PREFIX'] + '%s')
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        raise InvalidUsageException(result.get('error'), 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        raise InvalidUsageException(
            "Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != current_app.config['CLIENT_ID']:
        raise InvalidUsageException(
            "Token's client ID does not match app's.", 401)

    session['access_token'] = access_token

    # Request user info
    params = {'access_token': access_token, 'alt': 'json'}
    data = requests.get(
        current_app.config['ME_INFO_URL'], params=params).json()
    social_id = 'gplus$' + data['id']
    name = data['name']
    pic_url = data['picture']
    email = data['email']
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # Add user to database
        user = User(
            social_id=social_id, name=name, pic_url=pic_url, email=email)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    flash('Log in successful.')
    next = session.get('next')
    if next is not None:
        del session['next']
        return url_for('main.index', _external=True) + next[1:]
    return url_for('main.index', _external=True)


@auth.route('/logout')
@login_required
def logout():
    """Log user out by disconnecting from the Gooogle account."""

    # Check if the token exists
    if session['access_token'] is None:
        raise InvalidUsageException(
            result.get('Current user not connected.'), 401)

    # Revoke the token
    url = current_app.config[
        'DISCONNECTION_URL_PREFIX'] + session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # CLean up stored token
        del session['access_token']
        logout_user()
        flash('Log out successful.')
        return redirect(url_for('main.index'))
    else:
        # For whatever reason, the given token was invalid.
        raise InvalidUsageException(
            result.get('Failed to revoke token for given user.'), 400)
