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
    """Add a new todo item"""
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

def mark_todo_as_completed(todo_id):
    session = Session()
    todo = session.query(Todo).filter_by(id=todo_id).first()
    if todo:
        todo.is_completed = True
        session.commit()
        success = True
    else:
        success = False
    session.close()
    return success

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
        # Build the base query
        query = session.query(Todo)

        # Apply category filter if needed
        if category != 'all':
            query = query.filter_by(category=category)

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        todos = query.order_by(Todo.created_at.desc()).offset(offset).limit(limit).all()

        return todos, total_count

    finally:
        session.close()
