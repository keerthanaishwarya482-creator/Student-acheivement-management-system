import mysql.connector


# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ishu246@#",
    database="student_achievement_db"
)

cursor = db.cursor()


def add_achievement():
    name = input("Enter student name: ")
    achievement = input("Enter achievement: ")
    category = input("Enter category: ")
    year = int(input("Enter year: "))

    sql = """
    INSERT INTO achievements
    (student_name, achievement_name, category, achievement_year)
    VALUES (%s, %s, %s, %s)
    """

    values = (name, achievement, category, year)

    cursor.execute(sql, values)
    db.commit()

    print("Achievement added successfully!")


def view_achievements():
    cursor.execute("SELECT * FROM achievements")
    records = cursor.fetchall()

    if not records:
        print("No achievements found.")
    else:
        print("\n--- Student Achievements ---")

        for record in records:
            print("Achievement ID:", record[0])
            print("Student Name:", record[2])
            print("Achievement:", record[4])
            print("Category:", record[5])
            print("Year:", record[6])
            print("----------------------------")


def search_achievement():
    search = input("Enter achievement to search: ")

    sql = """
    SELECT * FROM achievements
    WHERE achievement_name LIKE %s
    """

    cursor.execute(sql, ("%" + search + "%",))
    records = cursor.fetchall()

    if records:
        print("\nAchievement Found!")

        for record in records:
            print("Student Name:", record[2])
            print("Achievement:", record[4])
            print("Category:", record[5])
            print("Year:", record[6])
    else:
        print("Achievement not found.")


def edit_achievement():
    name = input("Enter student name to edit: ")

    sql = "SELECT * FROM achievements WHERE student_name = %s"
    cursor.execute(sql, (name,))
    record = cursor.fetchone()

    if record:
        new_achievement = input("Enter new achievement: ")
        new_category = input("Enter new category: ")
        new_year = int(input("Enter new year: "))

        update_sql = """
        UPDATE achievements
        SET achievement_name = %s,
            category = %s,
            achievement_year = %s
        WHERE student_name = %s
        """

        values = (new_achievement, new_category, new_year, name)

        cursor.execute(update_sql, values)
        db.commit()

        print("Achievement updated successfully!")
    else:
        print("Student not found.")


def delete_achievement():
    name = input("Enter student name to delete: ")

    sql = "DELETE FROM achievements WHERE student_name = %s"
    cursor.execute(sql, (name,))
    db.commit()

    if cursor.rowcount > 0:
        print("Achievement deleted successfully!")
    else:
        print("Student not found.")


while True:
    print("\n===== Student Achievement Management System =====")
    print("1. Add Achievement")
    print("2. View Achievements")
    print("3. Search Achievement")
    print("4. Edit Achievement")
    print("5. Delete Achievement")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_achievement()

    elif choice == "2":
        view_achievements()

    elif choice == "3":
        search_achievement()

    elif choice == "4":
        edit_achievement()

    elif choice == "5":
        delete_achievement()

    elif choice == "6":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")


cursor.close()
db.close()
