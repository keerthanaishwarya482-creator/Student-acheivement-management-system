import json

FILE = "achievements.json"

# Load saved data
try:
    with open(FILE, "r") as file:
        achievements = json.load(file)
except:
    achievements = []


def save_data():
    with open(FILE, "w") as file:
        json.dump(achievements, file, indent=4)


def add_achievement():
    name = input("Enter student name: ")
    achievement = input("Enter achievement: ")
    category = input("Enter category: ")
    year = input("Enter year: ")

    record = {
        "name": name,
        "achievement": achievement,
        "category": category,
        "year": year
    }

    achievements.append(record)
    save_data()

    print("Achievement added and saved!")


def view_achievements():
    if not achievements:
        print("No achievements found.")
    else:
        print("\n--- Student Achievements ---")

        for record in achievements:
            print("Student Name:", record["name"])
            print("Achievement:", record["achievement"])
            print("Category:", record["category"])
            print("Year:", record["year"])
            print("----------------------------")


def search_achievement():
    search = input("Enter achievement to search: ")

    for record in achievements:
        if search.lower() in record["achievement"].lower():
            print("\nAchievement Found!")
            print("Student Name:", record["name"])
            print("Achievement:", record["achievement"])
            print("Category:", record["category"])
            print("Year:", record["year"])
            return

    print("Achievement not found.")


def edit_achievement():
    name = input("Enter student name to edit: ")

    for record in achievements:
        if record["name"].lower() == name.lower():
            record["achievement"] = input("Enter new achievement: ")
            record["category"] = input("Enter new category: ")
            record["year"] = input("Enter new year: ")

            save_data()
            print("Achievement updated and saved!")
            return

    print("Student not found.")


def delete_achievement():
    name = input("Enter student name to delete: ")

    for record in achievements:
        if record["name"].lower() == name.lower():
            achievements.remove(record)
            save_data()
            print("Achievement deleted!")
            return

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
