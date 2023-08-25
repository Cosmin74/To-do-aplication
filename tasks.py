from flask import Blueprint, jsonify, request, render_template
from model import Task
from user import User
from peewee import JOIN
from users import *

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    id_user_task = id_for_task()
    tasks = (Task
         .select(Task.task_id, Task.task_title, Task.task_description, Task.task_state)
         .join(User, join_type=JOIN.INNER, on=(id_user_task == Task.user_id)))
    unique_tasks = list(set(tasks))    
    return render_template('tasks.html', tasks=unique_tasks)

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    id_user_task = id_for_task()
    task = Task.select(Task.task_id, Task.task_title, Task.task_description, Task.task_state).join(User, join_type=JOIN.INNER, on=(id_user_task == Task.user_id)).where(Task.task_id == task_id).first()
    if task:
        return render_template('task.html', task=task)
    else:
        return jsonify({"error": "Task not found."}), 404

@task_bp.route('/submit_task', methods=['POST'])
def submit_task():
    id_user_task = id_for_task()
    task_title = request.form.get('task_title')
    task_description = request.form.get('task_description')  
    task = Task(task_title=task_title, task_description=task_description, user_id=id_user_task)
    task.save()
    return """
    <script>
        alert('Task submitted successfully!');
        window.location.href = '/tasks'; 
    </script>
    """

@task_bp.route('/tasks/<int:task_id>', methods=['POST', 'DELETE','PUT'])
def delete_task(task_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'delete':
            try:
                task = Task.get(Task.task_id == task_id)
                task.delete_instance()
                return  """
                <script>
                    alert('Task deleted successfully!');
                     window.location.href = '/tasks'; 
                </script>
                """
            except Task.DoesNotExist:
                return jsonify({"error": "Task not found."}), 404
            
        elif request.form.get('_method_1') == 'put':
            try:
                task = Task.get(Task.task_id == task_id)
                task.task_state = 'Completed'
                task.save()
                return  """
                <script>
                    alert('Task updated successfully!');
                     window.location.href = '/tasks'; 
                </script>
                """
            except Task.DoesNotExist:
                return jsonify({"error": "Task not found."}), 404