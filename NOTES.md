# Random notes

## API

### CRUD

Ref: <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>

| Operation        | SQL    | HTTP               | RESTful WS | DDS         | MongoDB |
| :--------------- | :----- | :----------------- | :--------- | :---------- | :------ |
| Create           | INSERT | PUT / POST         | POST       | write       | Insert  |
| Read (Retrieve)  | SELECT | GET                | GET        | read / take | Find    |
| Update (Modify)  | UPDATE | PUT / POST / PATCH | PUT        | write       | Update  |
| Delete (Destroy) | DELETE | DELETE             | DELETE     | dispose     | Remove  |

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

Ref: <https://www.restapitutorial.com/lessons/httpmethods.html>

| HTTP Verb | CRUD           | Entire Collection (e.g. /customers) Specific Item (e.g. /customers/{id}) |
| :-------- | :------------- | :----------------------------------------------------------------------- |
| POST      | Create         | 201 (Created), 'Location' header with link to /customers/{id} containing new ID. 404 (Not Found), 409 (Conflict) if resource already exists.. |
| GET       | Read           | 200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists. 200 (OK), single customer. 404 (Not Found), if ID not found or invalid. |
| PUT       | Update/Replace | 405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection. 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| PATCH     | Update/Modify  | 405 (Method Not Allowed), unless you want to modify the collection itself. 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| DELETE    | Delete         | 405 (Method Not Allowed), unless you want to delete the whole collection--not often desirable. 200 (OK). 404 (Not Found), if ID not found or invalid. |

## API testing tool:

- [Postman](https://www.getpostman.com/) -- This tool basically allows you to test your API endpoints, observe the responses. You can go even further to create scripts and do automated testing.
- [Insomnia](https://insomnia.rest/) -- An open source alternative to Postman. It comes with all the basic features you will need for API endpoints testing, and a better design IMO.

## Flask server

- Ref: <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world> (23 chapters!)
- Ref: <https://dev.to/duomly/how-to-create-a-simple-rest-api-with-python-and-flask-in-5-minutes-3edg>
- Ref: <https://pybit.es/simple-flask-api.html>
- Ref: <https://pythonhosted.org/Flask-Security/>

- Following is Ref: <https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699>

### server side

```
$ python3 -m venv venv
$ . venv/bin/activate
$ python3 -m pip install Flask
$ cat > minimal-flask-app.py <<EOM
from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return 'Hello from Server'
EOM

$ export FLASK_ENV=development
$ export FLASK_APP=minimal-flask-app.py
$ flask run
```

### client side testing

```
$ unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/greet
```

### app routing

```
$ cat > flask-app-routing.py <<EOM
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  return 'Index Page'

@app.route('/hello')
def hello():
  return 'Hello, greetings from different endpoint'

#adding variables
@app.route('/user/<username>')
def show_user(username):
  #returns the username
  return 'Username: %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
  #returns the post, the post_id should be an int
  return str(post_id)
EOM

$ export FLASK_APP=flask-app-routing.py
$ flask run
```

### GET, POST method

```
$ cat > methods.py <<EOM
from flask import Flask, request
app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    #check user details from db
    login_user()
  elif request.method == 'GET':
    #serve login page
    serve_login_page()
EOM
```

### Templates

```
$ cat > render-template.py <<EOM
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/user/<name>')
def hello(name=None):
  #name=None ensures the code runs even when no name is provided
  return render_template('user-profile.html', name=name)
EOM
```

See also <http://jinja.pocoo.org/>

### Authentication

```
$ cat > accessing-request-data.py <<EOM
from flask import Flask, request
app = Flask(__name__)

@app.route('/user', methods=['GET','POST'])
def get_user():
  username = request.form['username']
  password = request.form['password']
  #login(arg,arg) is a function that tries to log in and returns true or false
  status = login(username, password)
  return status
EOM
```

To access parameters submitted in the URL (`?key=value`) you can use the args attribute.

`searchkeyword = request.args.get('key': '')`

It's recommended to catch `KeyError` when using URL parameters as some users can change the URL which may return a Bad Request error page.

### File Uploads

Flask allows you to upload files from a form object, just make sure you set `enctype="multipart/form-data"` attibute on your form. You can access your file using the hostname of your server plus the file directory i.e `https://myapp.com/var/www/uploads/profilephoto.png` after saving to the file system.

```
$ cat > file-upload.py <<EOM
from flask import Flask, request
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        static_file = request.files['the_file']
        # here you can send this static_file to a storage service
        # or save it permanently to the file system
        static_file.save('/var/www/uploads/profilephoto.png')
EOM
```

## Tips

Ref: <https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask>

Code: <https://gist.github.com/miguelgrinberg/5614326>

### Error handling

```
$ cat > app.py <<EOM
from flask import abort

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run(debug=True)
EOM
```

Since this is a web service client applications will expect that we always respond with JSON, so we need to improve our 404 error handler:

```
from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
```

### Content type verification

```
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
```

### Authentication

Add module: `pip install flask-httpauth`

```
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# alternative - better for browser, but not standards compliant...
#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})
```

## JSON, DB backend

Ref: <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>

### Return JSON

```
$ cat > search-json.py <<EOM
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()

EOM

$ python3 search-json.py
```

### DB

```
$ cat > db-api.py <<EOM
import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

# driver function
if __name__ == '__main__':
     app.run(debug = True)
EOM

$ python3 db-api.py
```

## Use Resource and API objects

Ref: <https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/>

```
$ cat > flask-restful.py <<EOM

# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):

        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):

        data = request.get_json()     # status code
        return jsonify({'data': data}), 201


# another resource to calculate the square of a number
class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(square, '/square/<int:num>')


# driver function
if __name__ == '__main__':

    app.run(debug = True)

EOM
```

## Resource full sample app

Ref: <https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3>

```
$ cat > app.py <<EOM
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200

api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
EOM
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

