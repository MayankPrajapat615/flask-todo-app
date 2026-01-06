from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app import db
from app.models.task import Task
from app.utils.auth import login_required
from sqlalchemy import case, func

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/view')
@login_required
def view_tasks():

    sort_by = request.args.get('sort', 'id')
    query = Task.query.filter_by(user_id=session['user_id'])

    if sort_by == 'title':
        query = query.order_by(func.lower(Task.title).asc())
    elif sort_by == 'status':
        custom_order = case(
            (Task.status == 'Pending', 1),
            (Task.status == 'Completed', 2),
        )
        query = query.order_by(custom_order, func.lower(Task.title).asc())
    else:
        query = query.order_by(Task.id.desc())

    tasks = query.all()

    return render_template('task.html', tasks = tasks, sort_by=sort_by)

@tasks_bp.route('/add', methods = ["POST"])
@login_required
def add_task(): 
    
    title = request.form.get('title')

    if title:
        task = Task(
            title=title,
            user_id=session['user_id']   # 🔴 BIND TASK TO USER HERE
        )
        db.session.add(task)
        db.session.commit()
        flash('task added successfully', 'success')
    
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
@login_required
def toggle_status(task_id):
    
    task = Task.query.filter_by(
        id=task_id,
        user_id=session['user_id']
    ).first()
    
    if not task:
        return "Unauthorized", 403

    if task:
        if task.status == 'Pending':
            task.status = 'Completed'
        else:
            task.status = 'Pending'
        
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id = task_id,
        user_id = session['user_id']
    ).first()

    if not task:
        return "Unauthorized", 403

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods =["POST"])
@login_required
def clear_tasks():

    Task.query.filter_by(
        user_id=session['user_id']
    ).delete()

    db.session.commit()
    flash("All tasks cleared!", 'info')
    return redirect(url_for('tasks.view_tasks'))
    