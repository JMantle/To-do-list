from flask import Flask, render_template, request, redirect
import sqlite3

def check_return(return_page):
    if return_page == "index":
        return "/"
    elif return_page == "completed":
        return "/completed_tasks"
    else:
        print("error returning")
        return "/"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add_task():
    content = request.form["content"]
    conn = get_db_connection()
    conn.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>/<string:return_page>", methods=["POST"])
def delete_task(id, return_page):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return_spot = check_return(return_page)
    return redirect(return_spot)

@app.route("/edit/<int:id>", methods=["GET"])
def edit_task(id):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", task = task)

@app.route("/done_edit/<int:id>", methods=["POST"])
def update_task(id):
    content = request.form["content"]
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET content = ? WHERE id = ?", (content, id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/complete/<int:id>", methods=["POST"])
def complete_task(id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/completed_tasks", methods = ["GET"])
def check_completed():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE completed = 1").fetchall()
    conn.close()
    return render_template("completed.html", tasks = tasks)

@app.route("/uncomplete/<int:id>", methods = ["POST"])
def uncomplete_task(id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/completed_tasks")
    


@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE completed = ?", (0,)).fetchall()
    conn.close()
    return render_template("index.html", tasks = tasks)



if __name__ == "__main__":
    app.run(debug=True)
