# JDapp .. playing with API and tasks

**Challenge:**

Write a Restful API that roughly mimics the API that Docker Engine provides..
(current specs are [here](https://docs.docker.com/engine/api/v1.40/))

**Warning:**
This is for educational purposes only and not suitable for anything at all..

## Image building

There are two Dockerfile's for building images included:
- Dockerfile.python3 utilizes the official python-3 image (~960 MB) and ends up around 1 GB.
- Dockerfile.debian  utilizes the bullseye-slim image (~76 MB) and ends up around 440 MB.


## API

### CRUD

Ref: <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>

| Operation        | SQL    | HTTP               | RESTful WS | DDS         | MongoDB |
| :--------------- | :----- | :----------------- | :--------- | :---------- | :------ |
| Create           | INSERT | PUT / POST         | POST       | write       | Insert  |
| Read (Retrieve)  | SELECT | GET                | GET        | read / take | Find    |
| Update (Modify)  | UPDATE | PUT / POST / PATCH | PUT        | write       | Update  |
| Delete (Destroy) | DELETE | DELETE             | DELETE     | dispose     | Remove  |

Ref: <https://www.restapitutorial.com/lessons/httpmethods.html>

| HTTP Verb | CRUD           | Entire Collection (e.g. /customers) Specific Item (e.g. /customers/{id}) |
| :-------- | :------------- | :----------------------------------------------------------------------- |
| POST      | Create         | 201 (Created), 'Location' header with link to /customers/{id} containing new ID. 404 (Not Found), 409 (Conflict) if resource already exists.. |
| GET       | Read           | 200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists. 200 (OK), single customer. 404 (Not Found), if ID not found or invalid. |
| PUT       | Update/Replace | 405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection. 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| PATCH     | Update/Modify  | 405 (Method Not Allowed), unless you want to modify the collection itself. 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| DELETE    | Delete         | 405 (Method Not Allowed), unless you want to delete the whole collection--not often desirable. 200 (OK). 404 (Not Found), if ID not found or invalid. |

## API code and endpoints

Ref: <https://pybit.es/simple-flask-api.html>

To create a simple API you implement one or more HTTP methods, in this case the following endpoints:

```
@app.route('/api/v1.0/items', methods=['GET'])
@app.route('/api/v1.0/items/<int:id>', methods=['GET'])
@app.route('/api/v1.0/items', methods=['POST'])
@app.route('/api/v1.0/items/<int:id>', methods=['PUT'])
@app.route('/api/v1.0/items/<int:id>', methods=['DELETE'])
```

## API testing tools:

- [Postman](https://www.getpostman.com/) -- This tool basically allows you to test your API endpoints, observe the responses. You can go even further to create scripts and do automated testing.
- [Insomnia](https://insomnia.rest/) -- An open source alternative to Postman. It comes with all the basic features you will need for API endpoints testing, and a better design IMO.

## Flask server

Flask -> Flask-Restful		(simple)
Flask -> Flask-Restplus	(adds classes and swagger)
Flask -> Flask-RestX		(community fork of flask-restplus)

### run server in python virtual environment

```
$ python3 -m venv venv
$ . venv/bin/activate
$ python3 -m pip install -r requirements.txt
$ export FLASK_ENV=development
$ export FLASK_APP=flask-app.py
$ flask run
```

### client side testing

```
$ unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/api-endpoint
```


## CURL tests

```
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
sqlite3 app.db .dump

curl -kLD - http://127.0.0.1:5000/
curl -kLD - http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin: http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items/0
curl -kLD - -u admin:password -H "Content-Type: application/json" -X POST -d '{ "name": "name1", "value":"value1" }' http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password -H "Content-Type: application/json" -X POST -d '{ "name": "name2", "value":"value2" }' http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password -H "Content-Type: application/json" -X POST -d '{ "name": "name3", "value":"value3" }' http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items/3
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items/4
curl -kLD - -u admin:password  -X DELETE http://127.0.0.1:5000/api/v1.0/items/2
curl -kLD - -u admin:password -H "Content-Type: application/json" -X PUT -d '{ "name": "newname3", "value":"novalue" }' http://127.0.0.1:5000/api/v1.0/items/3
curl -kLD - -u admin:password  http://127.0.0.1:5000/api/v1.0/items
curl -kLD - -H "Authorization: Bearer eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MzM0MzQxMSwiZXhwIjoxNTkzMzQ3MDEx9Q" http://127.0.0.1:5000/api/v1.0/items
```

