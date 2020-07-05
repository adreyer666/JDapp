#!/usr/bin/env python3

from flask import request
from flask_restx import Resource, reqparse
# from JDlib import DataDB, Tasker

# --------- restful class --------------------------------------------------


class items(Resource):
    """
    Test module with id/key/value DB storage backend.
    Simple class for testing purposes.
    """

    def __init__(self, *args, **kwargs):
        """
        Update internal class default values if needed.

        :param verbose:     set verbosity level for debug and logging
        :param decorators:  apply decorators for access control
        :param datadb:      backend database
        :returns str: An endpoint name
        """

        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']
        else:
            self.verbose = 0
        if 'decorators' in kwargs:
            self.method_decorators = kwargs['decorators']
        else:
            self.method_decorators = []
        if 'datadb' in kwargs:
            self.datadb = kwargs['datadb']
        else:
            self.datadb = None

    def get(self, id=None):
        """
        Get item entry from DB.

        :param id:      uniq item *id*
        :returns str:   item value
        """
        if self.verbose:
            print("get id:", id, "\nverbose:", self.verbose)
        if id is None:
            items = self.datadb.data_get_byid()
        else:
            items = self.datadb.data_get_byid(id)
        if not items:
            return {"error": "Not found "+request.url}, 404
        return {"items": items}, 200

    def post(self, id=None):
        """Add item entry to DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("value")
        args = parser.parse_args()

        if id is not None:
            return {"error": "Bad request"}, 400
        if self.datadb.data_get_byname(args['name']):
            return {"error": "Conflict"}, 409
        item = {"name": args['name'], "value": args['value']}
        self.datadb.data_add(item)
        item['id'] = self.datadb.data_get_byname(args['name'])
        return {'item': item}, 201

    def put(self, id=None):
        """Update item entry in DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("value")
        args = parser.parse_args()

        if id is None:
            return {"error": "Method Not Allowed"}, 405
        item = self.datadb.data_get_byid(id)
        if not item:
            return {"error": "Not found "+request.url}, 404
        newitem = {
            "id": id,
            "name": (args['name'] if args['name'] else item['name']),
            "value": (args['value'] if args['value'] else item['value'])
        }
        self.datadb.data_update(newitem)
        return {'item': newitem}, 200

    def delete(self, id=None):
        """Don't try to delete the application entry point."""
        if id is None:
            return {"error": "Method Not Allowed"}, 405
        item = self.datadb.data_get_byid(id)
        if not item:
            return {"error": "Not found "+request.url}, 404
        self.datadb.data_delete(id)
        return {}, 204


# --------- implemented in main app or in calling class ----------------------

# # creating the flask app
# app = Flask(__name__)
# # creating an API object
# api = Api(app)
# # creating authentication objects
# app.config['SECRET_KEY'] = TOKENKEY
# basic_auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth('Bearer')
# multi_auth = MultiAuth(basic_auth, token_auth)
# datadb = DataDB(DB,'resource')
#
# # adding the defined resources along with their corresponding urls
# api.add_resource(items, '/api/v1.0/items', '/api/v1.0/items/<int:id>')

# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    print("items class for import into JDmodules framework")
    # resource_class_kwargs
