from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True, help="This field cannot be blank")
parser.add_argument('time', type=int, help='This field have to be an integer')

TODOS = {}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message=f"Todo {todo_id} doesn't exist")

class Todo(Resource):
    
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return jsonify(TODOS[todo_id])

    def put(self, todo_id):
        args = parser.parse_args()
        TODOS[todo_id] = {"task": args["task"], "time": args["time"]}
        return make_response(jsonify({todo_id: TODOS[todo_id]}), 201)
    
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return make_response(jsonify(TODOS), 204)

class Todos(Resource):
    def get(self):
        return jsonify(TODOS)

    def post(self, todo_id):
        args = parser.parse_args()
        if todo_id not in TODOS:
            TODOS[todo_id] = {"task": args["task"], "time": args["time"]}
            return make_response(jsonify({todo_id: TODOS[todo_id]}), 201)
        else:
            abort(400, message = f"Task {todo_id} already exists")


api.add_resource(Todo, 
    '/<string:todo_id>',
    '/todo/<string:todo_id>'
)

api.add_resource(Todos, 
    '/todos',
    '/todos/<string:todo_id>'
)

if __name__ == '__main__':
    app.run(debug=True)