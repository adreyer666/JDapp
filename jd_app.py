#!/usr/bin/env python3

"""
Flask application providing a RESTful API to do boring stuff.

Flask listens to http://127.0.0.1:5000/
API entry point is /api/v1/
"""

import os
import sys
from pprint import pprint
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_restx import Resource, Api

from jd_lib import AuthDB, DataDB, TaskMgr
from jd_modules import Items
# from jd_modules import Podman
from jd_modules.podman import Images as PodmanImages


DB = 'file:app.db'
TOKENKEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MzM0MzQxMSwiZXhwIjoxNTkzMzQ3MDEx9Q'
DEBUGIT = False  # True # False


# --------- debug ------------------------------------------------------------


def mydebug(*data):
    """Print information if global debug flag is set."""
    if DEBUGIT:
        pprint(data)
    return True


# --------- authentication handlers and callbacks ----------------------------


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    """Verify provided password credentials are valid for user."""
    authdata = None
    mydebug('username/password provided', username)
    if username:
        authdata = authdb.user_get(username)
    if authdata:
        if check_password_hash(authdata['password'], password):
            return username
    return False


@token_auth.verify_token
def verify_token(token):
    """Verify provided token credential is valid."""
    mydebug('token provided', token)
    data = authdb.token_get(token)
    if data and 'username' in data:
        return data['username']
    return False


@basic_auth.error_handler
@token_auth.error_handler
def unauthorized():
    """Throw error message (credentials invalid)."""
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# --------- restful resource classes -----------------------------------------


class TopLevel(Resource):
    """Simple resource to redirect to the correct entry point."""

    decorators = [multi_auth.login_required]

    def __init__(self, *args, **kwargs):
        """Update internal class default values if needed."""
        super().__init__(self, *args, **kwargs)
        self.debug = 0
        if self.debug > 2:
            print("args", args)
            print("kwargs", kwargs)
        if 'entrypoint' in kwargs:
            self.entrypoint = kwargs['entrypoint']
        else:
            self.entrypoint = '/api/v1.0'
        print(self.entrypoint)

    def get(self, subpath=None):
        """Redirect to correct entrypoint."""
        if self.debug:
            print("path", subpath)
        return redirect(self.entrypoint)

    def post(self, subpath=None):
        """Redirect to correct entrypoint."""
        if self.debug:
            print("path", subpath)
        return redirect(self.entrypoint)

    def put(self, subpath=None):
        """Redirect to correct entrypoint."""
        if self.debug:
            print("path", subpath)
        return redirect(self.entrypoint)

    def delete(self, subpath=None):
        """Redirect to correct entrypoint."""
        if self.debug:
            print("path", subpath)
        if ('FLASK_ENV' in os.environ) and \
           (os.environ['FLASK_ENV'] == 'development'):
            sys.exit(255)
        return redirect(self.entrypoint)


class ApiTop(Resource):
    """Application top level. This should give a welcome page..."""

    decorators = [multi_auth.login_required]

    def __init__(self, *args, **kwargs):
        """Update internal class default values if needed."""
        super().__init__(self, *args, **kwargs)
        # if debug:
        #     self.debug = debug
        # else:
        #     self.debug = 0
        self.debug = 0
        if self.debug > 2:
            print("args", args)
            print("kwargs", kwargs)

    def get(self):
        """Welcome greeting. Should need more info."""
        if self.debug:
            print("Login by user %s" % multi_auth.current_user())
        return {'message': 'Hello %s' % multi_auth.current_user()}

    def post(self):
        """Don't try to posting to the entry point. Bounces your data."""
        data = request.get_json()
        if self.debug:
            print("Data provided:\n%s" % data)
        return {'data': data}, 201

    def put(self):
        """Don't try to posting to the entry point. Bounces your data."""
        data = request.get_json()
        if self.debug:
            print("Data provided:\n%s" % data)
        return {'data': data}, 201

    def delete(self):
        """Don't try to delete the application entry point."""
        if self.debug:
            print("Trying to delete endpoint!")
        return {'message': 'denied'}


# --------- main -------------------------------------------------------------


# creating the flask app
app = Flask(__name__)
# creating authentication objects
app.config['SECRET_KEY'] = TOKENKEY


# @app.route('/')
# @multi_auth.login_required
# def index():
#     return "Hello, {}!".format(multi_auth.current_user())


# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    authdb = AuthDB(DB)
    datadb = DataDB(DB, 'resource')
    taskmgr = TaskMgr()

    # creating an API object
    api = Api(app)
    # adding the defined resources along with their corresponding urls
    api.add_resource(TopLevel,
                     '/', '/<path:subpath>',
                     resource_class_kwargs={'entrypoint': '/api/v1.0'})
    api.add_resource(ApiTop,
                     '/api/v1.0')
    api.add_resource(Items,
                     '/api/v1.0/items',
                     '/api/v1.0/items/<int:item_id>',
                     resource_class_kwargs={
                         'datadb': datadb,
                         'decorators': [multi_auth.login_required]
                         }
                     )
    # api.add_resource(Podman,
    #                  '/api/v1.0/podman',
    #                  '/api/v1.0/podman/<path:subpath>',
    #                  resource_class_kwargs={
    #                      'decorators': [multi_auth.login_required]
    #                      }
    #                  )
    api.add_resource(PodmanImages,
                     '/api/v1.0/podman/images',
                     '/api/v1.0/podman/images/<string:item_id>',
                     resource_class_kwargs={
                         'decorators': [multi_auth.login_required],
                         'taskmgr': taskmgr,
                         'verbose': 3
                         }
                     )

    app.run(debug=True)
