from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        try:
            return {todo_id: todos[todo_id]}
        except KeyError:
            return {"error": f"Task {todo_id} does not exist"}, 404
        except Exception as e:
            print(e)
            return {"error": "Unexpected error"}, 500

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return jsonify({todo_id: todos[todo_id]})
    
    def delete(self, todo_id):
        del todos[todo_id]
        return jsonify(todos)

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)