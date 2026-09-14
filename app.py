from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)


def connect_database():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        ssl_disabled=False
    )


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


@app.route("/")
def home():
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM achievements")
    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", achievements=achievements)


@app.route("/add", methods=["POST"])
def add():
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

    return redirect("/")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "")

    db = connect_database()
    cursor = db.cursor(dictionary=True)

    search_value = "%" + keyword + "%"

    cursor.execute("""
        SELECT * FROM achievements
        WHERE student_name LIKE %s
        OR achievement_name LIKE %s
        OR category LIKE %s
    """, (search_value, search_value, search_value))

    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", achievements=achievements)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
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

        return redirect("/")

    cursor.execute(
        "SELECT * FROM achievements WHERE achievement_id = %s",
        (id,)
    )

    achievement = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("edit.html", achievement=achievement)


@app.route("/delete/<int:id>")
def delete(id):
    db = connect_database()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM achievements WHERE achievement_id = %s",
        (id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect("/")


create_table()


if __name__ == "__main__":
    app.run(debug=True)
