from flask import jsonify

from database.database import get_categories_with_task_counts

def get_categories():
    try:
        # Get categories with task counts
        categories = get_categories_with_task_counts()

        return jsonify({
            'categories': categories
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500