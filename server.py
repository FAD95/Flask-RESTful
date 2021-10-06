from flask import Flask, request, jsonify
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
        return TODOS[todo_id]

    def put(self, todo_id):
        args = parser.parse_args()
        TODOS[todo_id] = {"task": args["task"], "time": args["time"]}
        return jsonify({todo_id: TODOS[todo_id]})
    
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return jsonify(TODOS)

api.add_resource(Todo, 
    '/<string:todo_id>',
    '/todos/<string:todo_id>'
)

if __name__ == '__main__':
    app.run(debug=True)