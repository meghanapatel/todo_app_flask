from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)


TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
        
tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:index>')
def edit_task(index):
    if 0 <= index < len(tasks):
        task = tasks[index]
        return render_template('edit.html', task=task, index=index)
    return redirect('/')

@app.route('/update/<int:index>', methods=['POST'])
def update_task(index):
    if 0 <= index < len(tasks):
        tasks[index] = request.form['task']
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

