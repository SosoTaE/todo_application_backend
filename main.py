from flask import Flask

from routes.ping import ping
from routes.get_todo import get_todo
from routes.add_todo import add_todos
from routes.update_todo import update_todos
from routes.delete_todo import delete_todos

app = Flask(__name__)

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

@app.route('/ping', methods=['GET'])
def ping_route():
    return ping()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)