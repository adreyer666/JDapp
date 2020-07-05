#!/usr/bin/env python3

"""
Podman image class.

Provided for educational purposes only.

    ┌────────┬────────────────────────┬───────────────────────────────────────┐
    │Command │ Man Page               │ Description                           │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │build   │ podman-build(1)        │ Build a container using a Dockerfile. │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │exists  │ podman-image-exists(1) │ Check if an image exists in local     │
    │        │                        │ storage.                              │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │history │ podman-history(1)      │ Show the history of an image.         │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │import  │ podman-import(1)       │ Import a tarball and save it as a     │
    │        │                        │ filesystem image.                     │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │inspect │ podman-inspect(1)      │ Display a image or image's            │
    │        │                        │ configuration.                        │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │list    │ podman-images(1)       │ List the container images on the      │
    │        │                        │ system.(alias ls)                     │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │load    │ podman-load(1)         │ Load an image from the docker         │
    │        │                        │ archive.                              │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │prune   │ podman-image-prune(1)  │ Remove all unused images from the     │
    │        │                        │ local store.                          │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │pull    │ podman-pull(1)         │ Pull an image from a registry.        │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │push    │ podman-push(1)         │ Push an image from local storage to   │
    │        │                        │ elsewhere.                            │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │rm      │ podman-rmi(1)          │ Removes one or more locally stored    │
    │        │                        │ images.                               │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │save    │ podman-save(1)         │ Save an image to docker-archive or    │
    │        │                        │ oci.                                  │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │sign    │ podman-image-sign(1)   │ Create a signature for an image.      │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │tag     │ podman-tag(1)          │ Add an additional name to a local     │
    │        │                        │ image.                                │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │untag   │ podman-untag(1)        │ Removes one or more names from a      │
    │        │                        │ locally-stored image.                 │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │tree    │ podman-image-tree(1)   │ Prints layer hierarchy of an image in │
    │        │                        │ a tree format.                        │
    ├────────┼────────────────────────┼───────────────────────────────────────┤
    │trust   │ podman-image-trust(1)  │ Manage container registry image trust │
    │        │                        │ policy.                               │
    └────────┴────────────────────────┴───────────────────────────────────────┘
"""

from time import sleep
from flask import request
from flask_restx import Resource, reqparse
# from jd_lib import DataDB, TaskMgr

# --------- restful class --------------------------------------------------


class Images(Resource):
    """
    Test module with id/key/value DB storage backend.

    Simple class for testing purposes.
    """

    def __init__(self, *args, **kwargs):
        """
        Update internal class default values if needed.

        :param verbose:     set verbosity level for debug and logging
        :param decorators:  apply decorators for access control
        :param taskmgr:     task manager for actions
        :returns str: An endpoint name
        """
        super().__init__(self, *args, **kwargs)
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
        if 'taskmgr' in kwargs:
            self.taskmgr = kwargs['datadb']
        else:
            self.taskmgr = None

    def _run_cmd(self, cmd=None) -> list:
        """Run command in foreground, report output."""
        if self.taskmgr is None:
            return None
        tid = self.taskmgr.add({"command": cmd})
        if tid is None:
            return None
        status = self.taskmgr.status(tid, verbose=True)
        maxcheck = 5
        while (status['status'] == 'running') and maxcheck:
            sleep(0.5)
            maxcheck -= 1
            status = self.taskmgr.status(tid, verbose=True)
        return status['stdout'], status['RC']

    def _build(self, tag=None) -> list:
        """
        podman-build(1).

        Build a container using a Dockerfile.
        """
        if self.verbose > 2:
            print(tag)
        item_list = []
        return item_list

    def _exists(self, uuid=None) -> bool:
        """
        podman-image-exists(1).

        Check if an image exists in local storage.
        """
        if self.verbose > 2:
            print(uuid)
        return True

    def _history(self) -> str:
        """
        podman-history(1).

        Show the history of an image.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _import(self) -> str:
        """
        podman-import(1).

        Import a tarball and save it as a filesystem image.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _inspect(self) -> str:
        """
        podman-inspect(1).

        Display a image or image's configuration.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _list(self, uuid=None) -> str:
        """
        podman-images(1).

        List the container images on the system.(alias ls)
        """
        cmd = "podman image list --format json"
        if uuid is not None:
            cmd += "--filter label %s" % uuid
        res = self._run_cmd(cmd)
        if res[0] is None:
            return [{'error': 'internal error'}]
        if res[1] == '':
            return [{'error': 'command still running'}]
        return res[0]

    def _load(self) -> str:
        """
        podman-load(1).

        Load an image from the docker archive.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _prune(self) -> str:
        """
        podman-image-prune(1).

        Remove all unused images from the local store.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _pull(self) -> str:
        """
        podman-pull(1).

        Pull an image from a registry.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _push(self) -> str:
        """
        podman-push(1).

        Push an image from local storage to elsewhere.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _rm(self, uuid=None) -> str:
        """
        podman-rmi(1).

        Removes one or more locally stored images.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_, uuid)
        return string_

    def _save(self, uuid=None) -> str:
        """
        podman-save(1).

        Save an image to docker-archive or oci.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_, uuid)
        return string_

    def _sign(self) -> str:
        """
        podman-image-sign(1).

        Create a signature for an image.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _tag(self) -> str:
        """
        podman-tag(1).

        Add an additional name to a local image.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _untag(self) -> str:
        """
        podman-untag(1).

        Removes one or more names from a locally-stored image.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _tree(self) -> str:
        """
        podman-image-tree(1).

        Prints layer hierarchy of an image in a tree format.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

    def _trust(self) -> str:
        """
        podman-image-trust(1).

        Manage container registry image trust policy.
        """
        string_ = ''
        if self.verbose > 2:
            print(string_)
        return string_

#
#

    def get(self, item_id=None):
        """
        Get item entry from DB.

        :param item_id:    unique image *id*
        :returns str:   image status
        """
        if self.verbose:
            print("get uuid:", item_id, "\nverbose:", self.verbose)

        parser = reqparse.RequestParser()
        parser.add_argument("action")
        args = parser.parse_args()

        if 'action' not in args:
            item_list = self._list(uuid=item_id)
        if not item_list:
            return {"error": "Not found "+request.url}, 404
        return {"images": item_list}, 200

    def post(self, item_id=None):
        """Add item entry to DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("action")
        parser.add_argument("name")
        args = parser.parse_args()

        if item_id is not None:
            return {"error": "Bad request"}, 400
        if 'action' not in args:
            return {"error": "Bad request"}, 400
        item = {"name": args['name'], "value": args['value']}
        if args['action'] == 'build':
            self._build(item)
        return {'images': [item]}, 201

    def put(self, item_id=None):
        """Update item entry in DB."""
        parser = reqparse.RequestParser()
        parser.add_argument("action")
        parser.add_argument("name")
        args = parser.parse_args()

        if item_id is None:
            return {"error": "Method Not Allowed"}, 405
        if 'action' not in args:
            return {"error": "Bad request"}, 400
        if not self._exists(item_id):
            return {"error": "Not found "+request.url}, 404
        newitem = {
            "id": item_id,
            "name": args['name'],
            "value": args['value']
        }
        self._save(newitem)
        return {'item': newitem}, 200

    def delete(self, item_id=None):
        """Don't try to delete the application entry point."""
        if item_id is None:
            return {"error": "Method Not Allowed"}, 405
        item = self._exists(item_id)
        if not item:
            return {"error": "Not found "+request.url}, 404
        self._rm(item_id)
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
    print("class for import into jd_modules framework")
    # resource_class_kwargs
