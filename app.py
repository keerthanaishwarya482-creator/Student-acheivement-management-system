from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)


# Connect to MySQL database
def connect_database():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        ssl_disabled=False
    )


# Create database table
def create_table():
    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            achievement_name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            achievement_year INT NOT NULL
        )
    """)

    db.commit()
    cursor.close()
    db.close()


# Robots.txt route for Google Search
@app.route("/robots.txt")
def robots():
    return """User-agent: *
Allow: /
"""


# Home page - view achievements
@app.route("/")
def index():
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM achievements ORDER BY achievement_id DESC")
    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", achievements=achievements)


# Add achievement
@app.route("/add", methods=["POST"])
def add_achievement():
    student_name = request.form["student_name"]
    achievement_name = request.form["achievement_name"]
    category = request.form["category"]
    achievement_year = request.form["achievement_year"]

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO achievements
        (student_name, achievement_name, category, achievement_year)
        VALUES (%s, %s, %s, %s)
    """, (
        student_name,
        achievement_name,
        category,
        achievement_year
    ))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("index"))


# Search achievement
@app.route("/search", methods=["GET", "POST"])
def search_achievement():
    search_query = request.args.get("query", "")

    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM achievements
        WHERE student_name LIKE %s
        OR achievement_name LIKE %s
        OR category LIKE %s
    """, (
        "%" + search_query + "%",
        "%" + search_query + "%",
        "%" + search_query + "%"
    ))

    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        achievements=achievements,
        search_query=search_query
    )


# Edit achievement
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_achievement(id):
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        student_name = request.form["student_name"]
        achievement_name = request.form["achievement_name"]
        category = request.form["category"]
        achievement_year = request.form["achievement_year"]

        cursor.execute("""
            UPDATE achievements
            SET student_name = %s,
                achievement_name = %s,
                category = %s,
                achievement_year = %s
            WHERE achievement_id = %s
        """, (
            student_name,
            achievement_name,
            category,
            achievement_year,
            id
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM achievements WHERE achievement_id = %s",
        (id,)
    )

    achievement = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "edit.html",
        achievement=achievement
    )


# Delete achievement
@app.route("/delete/<int:id>")
def delete_achievement(id):
    db = connect_database()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM achievements WHERE achievement_id = %s",
        (id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("index"))


# Create table when application starts
create_table()


if __name__ == "__main__":
    app.run(debug=True)
