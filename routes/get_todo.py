from database.database import get_all_todos, get_todos_by_category, get_paginated_todos

from flask import jsonify, request



def get_todo():
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Limit per_page to a reasonable number to prevent abuse
        if per_page > 100:
            per_page = 100

        # Get category filter (if any)
        category = request.args.get('category', 'all')

        # Calculate offset for pagination
        offset = (page - 1) * per_page

        # Get todos with pagination
        todos, total_count = get_paginated_todos(category, offset, per_page)

        # Convert todos to JSON-serializable format
        result = []
        for todo in todos:
            result.append({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'category': todo.category,
                'is_completed': todo.is_completed,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'due_date': todo.due_date.isoformat() if todo.due_date else None
            })

        # Calculate total pages
        total_pages = (total_count + per_page - 1) // per_page

        # Create pagination metadata
        pagination = {
            'page': page,
            'per_page': per_page,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }

        # Return todos with pagination info
        return jsonify({
            'todos': result,
            'pagination': pagination
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500