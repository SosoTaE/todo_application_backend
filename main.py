from flask import Flask
from flask_cors import CORS

from routes.ping import ping
from routes.get_todo import get_todo
from routes.add_todo import add_todos
from routes.update_todo import update_todos
from routes.delete_todo import delete_todos
from routes.get_categories import get_categories
from routes.complete_todo import complete_todo
from routes.login import login

from middleware.auth import authenticate_request

from config import Config
app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes

config = Config()

@app.route('/api/login', methods=['POST'])
def login_route():
    return login(config)

@app.before_request
def before_request():
    return authenticate_request(config)

@app.route('/api/todos')
def get_todo_route():
    return get_todo()

@app.route('/api/todo', methods=["POST"])
def add_todo_route():
    return add_todos()

@app.route("/api/todo/<int:id>", methods=["PUT"])
def update_todo_route(id):
    return update_todos(id)

@app.route("/api/todo/<int:id>", methods=["DELETE"])
def delete_todo_route(id):
    return delete_todos(id)

@app.route('/api/categories', methods=["GET"])
def get_categories_route():
    return get_categories()

@app.route('/api/todos/<int:id>/complete', methods=["PUT"])
def complete_todo_route(id):
    return complete_todo(id)

@app.route('/ping', methods=['GET'])
def ping_route():
    return ping()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)