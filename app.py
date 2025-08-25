from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

# --- Constants ---
DB_NAME = "todos.db"
PROJECT_ID = "DEV-OPS-2024-FLASK-PIPELINE"
STUDENT_NAME = "Soniya Kothari"  # Replace with your name/ID

# --- Create DB if it doesn't exist ---
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE todos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        done BOOLEAN NOT NULL DEFAULT 0
                    )''')
        conn.commit()
        conn.close()

# --- Home Route ---
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Add new task
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()

    # Get all tasks
    c.execute("SELECT id, task, done FROM todos")
    todos = c.fetchall()
    conn.close()

    # HTML Template
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <h1> Vansh to do list </h1>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f7f7f7; }
            h1 { color: #4CAF50; }
            form { margin-bottom: 20px; }
            input[type=text] { padding: 8px; width: 250px; }
            button { padding: 8px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
            ul { list-style-type: none; padding: 0; }
            li { background: white; margin: 5px 0; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
            .done { text-decoration: line-through; color: gray; }
        </style>
    </head>
    <body>
        
        <form method="POST">
            <input type="text" name="task" placeholder="Enter a new task" required>
            <button type="submit">Add</button>
        </form>
        <ul>
            {% for id, task, done in todos %}
                <li>
                    <span class="{{ 'done' if done else '' }}">{{ task }}</span>
                    <span>
                        <a href="{{ url_for('toggle_task', task_id=id) }}">[Toggle]</a>
                        <a href="{{ url_for('delete_task', task_id=id) }}">[Delete]</a>
                    </span>
                </li>
            {% endfor %}
        </ul>
        <p><strong>Project:</strong> {{ project_id }} | <strong>Prepared By:</strong> {{ student_name }}</p>
    </body>
    </html>
    """

    return render_template_string(html, todos=todos, project_id=PROJECT_ID, student_name=STUDENT_NAME)

# --- Toggle Task Status ---
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT done FROM todos WHERE id=?", (task_id,))
    current_status = c.fetchone()[0]
    c.execute("UPDATE todos SET done=? WHERE id=?", (0 if current_status else 1, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Delete Task ---
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Main ---
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
