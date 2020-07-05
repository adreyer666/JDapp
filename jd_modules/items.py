#!/usr/bin/env python3

"""
Flask resource class storing items.

Provided for testing purposes only.
"""

from flask import request
from flask_restx import Resource, reqparse
# from JDlib import DataDB, Tasker

# --------- restful class --------------------------------------------------


class Items(Resource):
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
        if self.verbose > 2:
            print("args", args)
            print("kwargs", kwargs)
        if 'decorators' in kwargs:
            self.method_decorators = kwargs['decorators']
        else:
            self.method_decorators = []
        if 'datadb' in kwargs:
            self.datadb = kwargs['datadb']
        else:
            self.datadb = None

    def get(self, item_id=None):
        """
        Get item entry from DB.

        :param item_id:      uniq item *id*
        :returns str:   item value
        """
        if self.verbose:
            print("get id:", item_id, "\nverbose:", self.verbose)
        if item_id is None:
            item_list = self.datadb.data_get_byid()
        else:
            item_list = self.datadb.data_get_byid(item_id)
        if not item_list:
            return {"error": "Not found "+request.url}, 404
        return {"items": item_list}, 200

    def post(self, item_id=None):
        """Add item entry to DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("value")
        args = parser.parse_args()

        if item_id is not None:
            return {"error": "Bad request"}, 400
        if self.datadb.data_get_byname(args['name']):
            return {"error": "Conflict"}, 409
        item = {"name": args['name'], "value": args['value']}
        self.datadb.data_add(item)
        item['id'] = self.datadb.data_get_byname(args['name'])
        return {'item': item}, 201

    def put(self, item_id=None):
        """Update item entry in DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("value")
        args = parser.parse_args()

        if item_id is None:
            return {"error": "Method Not Allowed"}, 405
        item = self.datadb.data_get_byid(item_id)
        if not item:
            return {"error": "Not found "+request.url}, 404
        newitem = {
            "id": item_id,
            "name": (args['name'] if args['name'] else item['name']),
            "value": (args['value'] if args['value'] else item['value'])
        }
        self.datadb.data_update(newitem)
        return {'item': newitem}, 200

    def delete(self, item_id=None):
        """Don't try to delete the application entry point."""
        if item_id is None:
            return {"error": "Method Not Allowed"}, 405
        item = self.datadb.data_get_byid(item_id)
        if not item:
            return {"error": "Not found "+request.url}, 404
        self.datadb.data_delete(id)
        return {}, 204


# --------- implemented in main app or in calling class ----------------------

# # creating the flask app
# app = Flask(__name__)
# api = Api(app)
# basic_auth = HTTPBasicAuth()
# datadb = DataDB(DB,'resource')
# api.add_resource(items, '/api/v1.0/items', '/api/v1.0/items/<int:id>',
#                  resource_class_kwargs={
#                      'datadb': datadb,
#                      'decorators': [basic_auth.login_required]
#                  })

# --------- main -------------------------------------------------------------


if __name__ == '__main__':
    print("items class for import into JDmodules framework")
    # resource_class_kwargs
