achievements = []

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
    print("Achievement added successfully!")


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


while True:

    print("\n===== Student Achievement Management System =====")
    print("1. Add Achievement")
    print("2. View Achievements")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_achievement()

    elif choice == "2":
        view_achievements()

    elif choice == "3":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")
