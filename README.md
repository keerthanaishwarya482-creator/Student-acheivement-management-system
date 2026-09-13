# Student-acheivement-management-system
A simple system that helps students record, organize, and manage their academic and extracurricular achievements in one place.
# Student Achievement Management System

## 📌 Project Overview

The **Student Achievement Management System** is a web-based application developed to store, manage, search, update, and delete student achievement details.

This system helps colleges maintain student achievements in an organized digital database instead of using manual records.

## 🎯 Problem Statement

Students participate in various activities such as academic events, sports, cultural programs, technical competitions, workshops, and seminars.

Managing these achievement records manually can be difficult and time-consuming. This project provides a simple digital solution to store and manage achievement information efficiently.

## 👥 Target Users

* College students
* Faculty members
* Department staff
* College administration

## ✨ Features

* Add new student achievements
* View all saved achievements
* Search achievements by student name
* Edit existing achievement details
* Delete achievement records
* Store data permanently in a MySQL database
* Simple and user-friendly web interface

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS

### Backend

* Python
* Flask

### Database

* MySQL

### Development Tools

* Visual Studio Code / Notepad
* Command Prompt
* Web Browser

## 🏗️ Project Structure

```text
Student Achievement Management System
│
├── app.py
│
└── templates
    ├── index.html
    └── edit.html
```

## 🗄️ Database Details

### Database Name

```text
student_achievement_db
```

### Table Name

```text
achievements
```

### Table Columns

| Column Name      | Description             |
| ---------------- | ----------------------- |
| achievement_id   | Unique achievement ID   |
| student_name     | Name of the student     |
| achievement_name | Name of the achievement |
| category         | Achievement category    |
| achievement_year | Year of achievement     |

## ⚙️ How to Run the Project

### Step 1: Install Python

Install Python on your computer.

### Step 2: Install Required Packages

Open Command Prompt and run:

```bash
pip install flask mysql-connector-python
```

### Step 3: Create the MySQL Database

Create the database and achievements table in MySQL.

### Step 4: Open the Project Folder

Open the project folder containing:

```text
app.py
templates
```

### Step 5: Run the Flask Application

Open Command Prompt in the project folder and run:

```bash
python app.py
```

### Step 6: Open the Website

Open a browser and visit:

```text
http://127.0.0.1:5000
```

## 🖥️ Main Modules

### 1. Add Achievement

Allows users to enter and save student achievement details.

### 2. View Achievements

Displays all achievement records stored in the database.

### 3. Search Achievement

Searches for achievements using the student name.

### 4. Edit Achievement

Allows users to update existing achievement information.

### 5. Delete Achievement

Removes unwanted achievement records from the database.

## ✅ Advantages

* Reduces manual paperwork
* Saves time
* Easy to maintain records
* Provides quick searching
* Supports updating and deleting records
* Stores information securely in a database

## 🚀 Future Enhancements

* Student login system
* Faculty login system
* Certificate upload feature
* Download achievement reports
* PDF report generation
* Dashboard with achievement statistics
* User authentication and security

## 📚 Conclusion

The Student Achievement Management System provides an efficient and simple way to manage student achievement records digitally. The combination of Python Flask and MySQL makes the system easy to develop, maintain, and expand in the future.

## 👩‍💻 Developer

**Name:** Ishwarya V
**Department:** Computer Science
**Project:** Student Achievement Management System
