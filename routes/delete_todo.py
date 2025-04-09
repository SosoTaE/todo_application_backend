from flask import jsonify

from database.database import delete_todo

def delete_todos(id):
    try:

        response = delete_todo(id)

        if response:
            return jsonify({"message": "Todo deleted successfully"}), 200

        return jsonify({"message": "Something went wrong"}), 500

    except Exception as e:
        return jsonify({"message": str(e)})