from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# Connect to MySQL database
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ishu246@#",
        database="student_achievement_db"
    )


# Home page - Display all achievements
@app.route("/")
def home():
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM achievements")
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

    sql = """
    INSERT INTO achievements
    (student_name, achievement_name, category, achievement_year)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        student_name,
        achievement_name,
        category,
        achievement_year
    )

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


# Search achievement
@app.route("/search")
def search_achievement():
    student_name = request.args.get("student_name", "")

    db = connect_database()
    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM achievements
    WHERE student_name LIKE %s
    """

    cursor.execute(sql, ("%" + student_name + "%",))
    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", achievements=achievements)


# Delete achievement
@app.route("/delete/<int:achievement_id>")
def delete_achievement(achievement_id):
    db = connect_database()
    cursor = db.cursor()

    sql = "DELETE FROM achievements WHERE achievement_id = %s"

    cursor.execute(sql, (achievement_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


# Open edit page
@app.route("/edit/<int:achievement_id>")
def edit_achievement(achievement_id):
    db = connect_database()
    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM achievements
    WHERE achievement_id = %s
    """

    cursor.execute(sql, (achievement_id,))
    achievement = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "edit.html",
        achievement=achievement
    )


# Update achievement
@app.route("/update/<int:achievement_id>", methods=["POST"])
def update_achievement(achievement_id):
    student_name = request.form["student_name"]
    achievement_name = request.form["achievement_name"]
    category = request.form["category"]
    achievement_year = request.form["achievement_year"]

    db = connect_database()
    cursor = db.cursor()

    sql = """
    UPDATE achievements
    SET student_name = %s,
        achievement_name = %s,
        category = %s,
        achievement_year = %s
    WHERE achievement_id = %s
    """

    values = (
        student_name,
        achievement_name,
        category,
        achievement_year,
        achievement_id
    )

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)