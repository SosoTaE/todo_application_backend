from datetime import datetime

from flask import request, jsonify
from database.database import update_todo

def update_todos(id):
    try:

        body = request.get_json()

        # Parse the date string to a datetime object
        due_date = None
        if 'due_date' in body and body['due_date']:
            try:
                # Parse date in format MM/DD/YYYY HH:MM
                due_date = datetime.strptime(body['due_date'], '%m/%d/%Y %H:%M:%S')
            except ValueError:
                return jsonify({"message": "Invalid date format. Use MM/DD/YYYY HH:MM:SS"}), 400


        response = update_todo(todo_id=id,
                           title=body.get("title"),
                           description=body.get("description"),
                           category=body.get("category"),
                           due_date=due_date)

        if response:
            return jsonify({"message":"Todo updated successfully"}), 200

        return jsonify({"message": "Something went wrong"}), 500

    except Exception as e:
        return jsonify({"message": str(e)})

