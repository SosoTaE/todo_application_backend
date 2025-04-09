from flask import request, jsonify

from database.database import mark_todo_completion

def complete_todo(id):
    try:
        data = request.get_json()
        is_completed = data.get('is_completed', True)

        success = mark_todo_completion(id, is_completed)

        if success:
            return jsonify({"message": f"Todo marked as {'completed' if is_completed else 'incomplete'}"})
        else:
            return jsonify({"message": "Todo not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500