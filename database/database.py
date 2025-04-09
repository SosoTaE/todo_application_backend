from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Todo(title='{self.title}', is_completed={self.is_completed})>"


# Create SQLite database engine
engine = create_engine('sqlite:///todo_app.db', echo=True)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Todo CRUD operations
def add_todo(title, category, description=None, due_date=None):
    session = Session()
    new_todo = Todo(
        title=title,
        category=category,
        description=description,
        due_date=due_date
    )
    session.add(new_todo)
    session.commit()
    todo_id = new_todo.id
    session.close()
    return todo_id

def get_all_todos():
    session = Session()
    todos = session.query(Todo).all()
    session.close()
    return todos

def get_todos_by_category(category):
    session = Session()
    todos = session.query(Todo).filter_by(category=category).all()
    session.close()
    return todos

def get_todo_by_id(todo_id):
    session = Session()
    todo = session.query(Todo).filter_by(id=todo_id).first()
    session.close()
    return todo

def get_incomplete_todos():
    session = Session()
    todos = session.query(Todo).filter_by(is_completed=False).all()
    session.close()
    return todos

def update_todo(todo_id, title=None, category=None, description=None, due_date=None):
    session = Session()
    todo = session.query(Todo).filter_by(id=todo_id).first()
    if todo:
        if title:
            todo.title = title
        if category is not None:
            todo.category = category
        if description is not None:
            todo.description = description
        if due_date is not None:
            todo.due_date = due_date
        session.commit()
        success = True
    else:
        success = False
    session.close()
    return success

def delete_todo(todo_id):
    session = Session()
    todo = session.query(Todo).filter_by(id=todo_id).first()
    if todo:
        session.delete(todo)
        session.commit()
        success = True
    else:
        success = False
    session.close()
    return success


def get_paginated_todos(category, offset=0, limit=10):
    session = Session()

    try:
        query = session.query(Todo)

        if category != 'all':
            query = query.filter_by(category=category)

        total_count = query.count()

        todos = query.order_by(Todo.created_at.desc()).offset(offset).limit(limit).all()

        return todos, total_count

    finally:
        session.close()


def get_categories_with_task_counts():
    session = Session()

    try:
        # Get all unique categories
        query = session.query(Todo.category).distinct().filter(Todo.category != None)
        categories = [category[0] for category in query.all()]

        result = []
        for category in categories:
            # Get total count for this category
            total_count = session.query(Todo).filter_by(category=category).count()

            # Get completed count for this category
            completed_count = session.query(Todo).filter_by(
                category=category,
                is_completed=True
            ).count()

            result.append({
                'name': category,
                'total_tasks': total_count,
                'completed_tasks': completed_count
            })

        # Sort by category name
        result.sort(key=lambda x: x['name'])

        return result

    finally:
        session.close()


def mark_todo_completion(todo_id, is_completed=True):
    session = Session()

    try:
        todo = session.query(Todo).filter_by(id=todo_id).first()

        if todo:
            todo.is_completed = is_completed
            session.commit()
            return True
        else:
            return False

    finally:
        session.close()