from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = 'tasks.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        """)
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_FILE) as conn:
        tasks = conn.execute("SELECT id, task, done FROM tasks").fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (task, False))
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
