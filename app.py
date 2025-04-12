from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            microscope_size REAL NOT NULL,
            magnification REAL NOT NULL,
            real_life_size REAL NOT NULL,
            unit TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- Home Route ----------
@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    init_db()  # 👈 Ensure table exists before any query

    if request.method == "POST":
        try:
            username = request.form["username"]
            microscope_size = float(request.form["microscope_size"])
            magnification = float(request.form["magnification"])
            unit = request.form["unit"]

            real_life_size = microscope_size / magnification

            conn = sqlite3.connect("specimen_data.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO specimens (username, microscope_size, magnification, real_life_size, unit)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, microscope_size, magnification, real_life_size, unit))
            conn.commit()
            conn.close()
            return redirect("/")
        except Exception as e:
            return f"Error in POST request: {e}", 400

    try:
        conn = sqlite3.connect("specimen_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM specimens")
        specimens = cursor.fetchall()
        conn.close()
        return render_template("index.html", specimens=specimens)
    except Exception as e:
        return f"Error rendering index.html or fetching data: {e}", 500

# ---------- Delete ----------
@app.route("/delete/<int:specimen_id>")
def delete(specimen_id):
    try:
        conn = sqlite3.connect("specimen_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM specimens WHERE id = ?", (specimen_id,))
        conn.commit()
        conn.close()
        return redirect("/")
    except Exception as e:
        return f"Error deleting record: {e}", 500

# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True)
