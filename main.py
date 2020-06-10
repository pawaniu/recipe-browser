# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import service
from flask import Flask
from flask import Flask, send_file, make_response, render_template, request,jsonify, send_from_directory, abort
from google.cloud import ndb

client = ndb.Client.from_service_account_json('pk-dev-service.json')


def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with client.context():
            return wsgi_app(environ, start_response)

    return middleware


app = Flask(__name__)
app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)


class Recipe(ndb.Model):
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    description = ndb.StringProperty()



@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/add-recipe')
def create():
    return render_template('create.html')


@app.route('/api/v1.0/recipes', methods=['POST'])
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    recipe = {
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'url': request.json.get('url', "")
    }
    response = service.create_recipe(recipe)
    resp = make_response(response)
    resp.status_code = 201
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/v1.0/recipes')
def recipes():
    recipes = Recipe.query()
    resp = make_response(str([recipe.to_dict() for recipe in Recipe.query()]))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=7000, debug=True)
# [END gae_flex_quickstart]
