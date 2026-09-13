from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "achievements.db"


# Connect to SQLite database
def connect_database():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


# Create database table
def create_table():
    db = connect_database()

    db.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            achievement_name TEXT NOT NULL,
            category TEXT NOT NULL,
            achievement_year INTEGER NOT NULL
        )
    """)

    db.commit()
    db.close()


# Home page - display all achievements
@app.route("/")
def home():
    db = connect_database()

    achievements = db.execute(
        "SELECT * FROM achievements"
    ).fetchall()

    db.close()

    return render_template(
        "index.html",
        achievements=achievements
    )


# Add achievement
@app.route("/add", methods=["POST"])
def add():
    student_name = request.form["student_name"]
    achievement_name = request.form["achievement_name"]
    category = request.form["category"]
    achievement_year = request.form["achievement_year"]

    db = connect_database()

    db.execute("""
        INSERT INTO achievements
        (student_name, achievement_name, category, achievement_year)
        VALUES (?, ?, ?, ?)
    """, (
        student_name,
        achievement_name,
        category,
        achievement_year
    ))

    db.commit()
    db.close()

    return redirect("/")


# Search achievement
@app.route("/search")
def search():
    keyword = request.args.get("keyword", "")

    db = connect_database()

    achievements = db.execute("""
        SELECT * FROM achievements
        WHERE student_name LIKE ?
        OR achievement_name LIKE ?
        OR category LIKE ?
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    )).fetchall()

    db.close()

    return render_template(
        "index.html",
        achievements=achievements
    )


# Edit achievement
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = connect_database()

    if request.method == "POST":
        student_name = request.form["student_name"]
        achievement_name = request.form["achievement_name"]
        category = request.form["category"]
        achievement_year = request.form["achievement_year"]

        db.execute("""
            UPDATE achievements
            SET student_name = ?,
                achievement_name = ?,
                category = ?,
                achievement_year = ?
            WHERE achievement_id = ?
        """, (
            student_name,
            achievement_name,
            category,
            achievement_year,
            id
        ))

        db.commit()
        db.close()

        return redirect("/")

    achievement = db.execute(
        "SELECT * FROM achievements WHERE achievement_id = ?",
        (id,)
    ).fetchone()

    db.close()

    return render_template(
        "edit.html",
        achievement=achievement
    )


# Delete achievement
@app.route("/delete/<int:id>")
def delete(id):
    db = connect_database()

    db.execute(
        "DELETE FROM achievements WHERE achievement_id = ?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect("/")


# Create table when application starts
create_table()


# Run application
if __name__ == "__main__":
    app.run(debug=True)
