from flask import render_template, session, request, current_app, \
    make_response, redirect, flash, url_for, abort
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .. import db
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import random
import string


@auth.route('/login')
def login():

    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state

    next = request.args.get('next')
    print next, 1111
    if next is not None:
        session['next'] = next

    return render_template('auth/login.html', state=state, client_id=current_app.config['CLIENT_ID'], next=next)


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ((current_app.config['TOKEN_INFO_URL_PREFIX'] + '%s')
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != current_app.config['CLIENT_ID']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # stored_access_token = session.get('access_token')
    # stored_gplus_id = session.get('gplus_id')
    # if stored_access_token is not None and gplus_id == stored_gplus_id:
    #     response = make_response(
    #         json.dumps('Current user is already connected.'), 200)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response

    # Store the access token in the session for later use.
    # session['access_token'] = access_token
    # session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user.', 200))

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
        user = User(
            social_id=social_id, name=name, pic_url=pic_url, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    # next = request.args.get('next')
    # print request.args
    # print next, 22222
    # if not next_is_valid(next):
    #     return abort(400)

    # flash("you are now logged in as %s" % name)
    flash('Log in successful.')
    next = session.get('next')
    # print url_for('main.index', _external=True) + next[1:]
    if next is not None:
        if not next_is_valid(next):
            return url_for('main.index', _external=True) + '404'
        del session['next']
        return url_for('main.index', _external=True) + next[1:]

    return url_for('main.index', _external=True)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out successful.')
    return redirect(url_for('main.index'))


def next_is_valid(next):
    return True
