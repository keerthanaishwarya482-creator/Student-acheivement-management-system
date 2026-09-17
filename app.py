from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)


# ---------------- DATABASE CONNECTION ----------------

def connect_database():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=False
    )


# ---------------- CREATE TABLE ----------------

def create_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            age INT,
            date_of_birth DATE,
            achievement_name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            achievement_year INT NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


create_table()


# ---------------- HOME PAGE ----------------

@app.route("/")
def index():
    connection = connect_database()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM achievements
        ORDER BY achievement_id DESC
    """)

    achievements = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", achievements=achievements)


# ---------------- ADD ACHIEVEMENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        student_name = request.form["student_name"]
        age = request.form["age"]
        date_of_birth = request.form["date_of_birth"]
        achievement_name = request.form["achievement_name"]
        category = request.form["category"]
        achievement_year = request.form["achievement_year"]

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO achievements
            (
                student_name,
                age,
                date_of_birth,
                achievement_name,
                category,
                achievement_year
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            student_name,
            age,
            date_of_birth,
            achievement_name,
            category,
            achievement_year
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add.html")


# ---------------- SEARCH ACHIEVEMENT ----------------

@app.route("/search", methods=["GET", "POST"])
def search():
    achievements = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        connection = connect_database()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM achievements
            WHERE student_name LIKE %s
            OR achievement_name LIKE %s
            OR category LIKE %s
        """, (
            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%"
        ))

        achievements = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "search.html",
        achievements=achievements
    )


# ---------------- EDIT ACHIEVEMENT ----------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    connection = connect_database()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        student_name = request.form["student_name"]
        age = request.form["age"]
        date_of_birth = request.form["date_of_birth"]
        achievement_name = request.form["achievement_name"]
        category = request.form["category"]
        achievement_year = request.form["achievement_year"]

        cursor.execute("""
            UPDATE achievements
            SET
                student_name=%s,
                age=%s,
                date_of_birth=%s,
                achievement_name=%s,
                category=%s,
                achievement_year=%s
            WHERE achievement_id=%s
        """, (
            student_name,
            age,
            date_of_birth,
            achievement_name,
            category,
            achievement_year,
            id
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM achievements WHERE achievement_id=%s",
        (id,)
    )

    achievement = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit.html",
        achievement=achievement
    )


# ---------------- DELETE ACHIEVEMENT ----------------

@app.route("/delete/<int:id>")
def delete(id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM achievements WHERE achievement_id=%s",
        (id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# ---------------- ROBOTS.TXT ----------------

@app.route("/robots.txt")
def robots():
    text = """User-agent: *
Allow: /
Sitemap: https://student-acheivement-management-system.onrender.com/sitemap.xml
"""

    response = app.response_class(
        response=text,
        status=200,
        mimetype="text/plain"
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


# ---------------- SITEMAP.XML ----------------

@app.route("/sitemap.xml")
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://student-acheivement-management-system.onrender.com/</loc>
    </url>
</urlset>"""

    return app.response_class(
        response=xml,
        status=200,
        mimetype="application/xml"
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)
