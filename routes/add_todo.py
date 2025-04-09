import json
from datetime import datetime

from flask import request, Response, jsonify

from database.database import add_todo

def add_todos():
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

        todo_id = add_todo(title=body.get("title"), category=body.get("category"), description=body.get("description"),
                           due_date=due_date)

        return Response(json.dumps({"todo_id": todo_id}), status=200, content_type="application/json")

    except Exception as e:
        return jsonify({"message": str(e)})