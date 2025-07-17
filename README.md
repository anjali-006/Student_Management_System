#  Student Management System

A web-based Student Management System built with **Flask** and **MySQL**, designed to simplify course, assignment, grade tracking, and resource management for educational institutions.

##  Features

-  User Authentication (Login & Signup with secure password hashing)
-  Add and manage:
  - Student Assignments and Marks
  - Courses
  - Library Resources
  - Announcements
-  Dashboard with:
  - Student marks aggregation (Total, Average, Max, Min)
  - Total course and student counts
-  Grade visualizations using Chart.js (via `/view_grades`)
-  Library Resource Tracking (with borrowing history)

---

##  Tech Stack

| Tech         | Purpose                     |
|--------------|-----------------------------|
| Flask        | Web framework (Python)      |
| MySQL        | Database                    |
| HTML/CSS     | Frontend structure/styling  |
| JavaScript   | Chart rendering (Chart.js)  |
| Jinja2       | Templating engine           |
| Git/GitHub   | Version control             |

---

##  Folder Structure

```
project_root/
│
├── static/                  # CSS, JS, and images
│   ├── style.css
│   ├── script.js
│   └── ...
│
├── templates/              # HTML templates (Jinja2)
│   ├── index.html.jinja2   # Login Page
│   ├── dashboard.html
│   ├── add_assignment.html
│   ├── add_course.html
│   ├── view_grades.html
│   ├── signup.html
│   └── announcements.html
│
├── kpflsk.py               # Main Flask app
└── README.md               # Project documentation
```

---

##  Installation

1. **Clone the repository:**

```bash
git clone https://github.com/anjali-006/Student_Management_System.git
cd Student_Management_System
```

2. **Install dependencies:**

Make sure you have Python 3 and pip installed.

```bash
pip install flask flask-mysqldb werkzeug
```

3. **Set up MySQL database:**

```sql
CREATE DATABASE project;

-- Table for user signup
CREATE TABLE signup (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  username VARCHAR(50) UNIQUE,
  password TEXT
);

-- Table for student marks
CREATE TABLE student_marks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_name VARCHAR(100),
  dbms_marks INT,
  econometrics_marks INT,
  math_marks INT,
  calculus_marks INT
);

-- Table for courses
CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_name VARCHAR(100),
  description TEXT,
  instructor VARCHAR(100),
  credits INT
);

-- Table for announcements
CREATE TABLE announcements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  message TEXT,
  author VARCHAR(100),
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_new BOOLEAN DEFAULT TRUE
);

-- Library Tables
CREATE TABLE LibraryResources (
  resource_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255),
  author VARCHAR(100),
  category VARCHAR(100),
  availability BOOLEAN
);

CREATE TABLE Borrowers (
  borrower_id INT PRIMARY KEY AUTO_INCREMENT,
  borrower_name VARCHAR(100)
);

CREATE TABLE BorrowHistory (
  history_id INT PRIMARY KEY AUTO_INCREMENT,
  resource_id INT,
  borrower_id INT,
  borrow_date DATE,
  return_date DATE,
  FOREIGN KEY (resource_id) REFERENCES LibraryResources(resource_id),
  FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);
```

4. **Update your MySQL credentials** in `kpflsk.py`:

```python
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
```

---

##  Run the App

```bash
python kpflsk.py
```

Then open your browser and go to:  
**`http://127.0.0.1:5000/`**

---

##  Sample User Flow

1. Sign up using `/signup`
2. Log in at `/login`
3. Access the dashboard at `/dashboard`
4. Add marks at `/addassignment`
5. Add courses via `/addcourse`
6. View charts at `/view_grades`
7. Check announcements via `/announcements`
8. Explore library data at `/library-resources`

---

##  Password Validation

- At least 8 characters
- One uppercase letter
- One lowercase letter
- One digit
- One special character

---
<img width="1835" height="950" alt="image" src="https://github.com/user-attachments/assets/d3fe9779-e345-4367-b305-9010c2be6b43" />
<img width="1842" height="886" alt="image" src="https://github.com/user-attachments/assets/18fe9b78-a1ce-4050-82dc-1775cd33bbbe" />
<img width="1886" height="965" alt="image" src="https://github.com/user-attachments/assets/6e2f93a4-0e5c-45c2-a2c5-29a70b5ecd19" />
<img width="1889" height="907" alt="image" src="https://github.com/user-attachments/assets/ce9335c5-c9cd-46ab-8828-4b94f0b087d3" />
<img width="1911" height="666" alt="image" src="https://github.com/user-attachments/assets/4ca24f1c-23ce-41a4-9974-c89c6016e539" />
<img width="1915" height="915" alt="image" src="https://github.com/user-attachments/assets/ecd6cf36-4ceb-490f-aad7-a8d44f1d7fde" />


