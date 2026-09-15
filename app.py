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


create_table()


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM achievements
        ORDER BY achievement_id DESC
    """)

    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        achievements=achievements
    )


# ---------------- ADD ACHIEVEMENT ----------------

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

    return redirect(url_for("home"))


# ---------------- SEARCH ACHIEVEMENT ----------------

@app.route("/search")
def search_achievement():
    keyword = request.args.get("keyword", "")

    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM achievements
        WHERE student_name LIKE %s
        OR achievement_name LIKE %s
        OR category LIKE %s
        ORDER BY achievement_id DESC
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        achievements=achievements,
        keyword=keyword
    )


# ---------------- EDIT ACHIEVEMENT ----------------

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

        return redirect(url_for("home"))

    cursor.execute("""
        SELECT * FROM achievements
        WHERE achievement_id = %s
    """, (id,))

    achievement = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "edit.html",
        achievement=achievement
    )


# ---------------- DELETE ACHIEVEMENT ----------------

@app.route("/delete/<int:id>")
def delete_achievement(id):
    db = connect_database()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM achievements
        WHERE achievement_id = %s
    """, (id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("home"))


# ---------------- ROBOTS.TXT ----------------

@app.route("/robots.txt")
def robots():
    response = app.response_class(
        response="User-agent: *\nAllow: /\nSitemap: https://student-acheivement-management-system.onrender.com/sitemap.xml\n",
        status=200,
        mimetype="text/plain"
    )

    response.headers["Cache-Control"] = (
        "no-cache, no-store, must-revalidate"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


# ---------------- SITEMAP.XML ----------------

@app.route("/sitemap.xml")
def sitemap():
    response = app.response_class(
        response="""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://student-acheivement-management-system.onrender.com/</loc>
    </url>
</urlset>
""",
        status=200,
        mimetype="application/xml"
    )

    return response


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)
