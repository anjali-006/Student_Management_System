from flask import Flask, request, flash, redirect, url_for, render_template,jsonify,session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = '12345'  # Replace with a strong, unique key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AnjaliSQL2006'  # Use your actual MySQL password
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

# Route for rendering the login page and storing data
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate username and password
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, password FROM signup WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user and user[1] == password:  # Replace with proper password hashing verification
            # Store the user's name in the session
            session['name'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
        
        cur.close()

    return render_template('index.html')
  # Login page
  # Renders the login page for GET requests
 # Render the login form

# Route for the dashboard page, displaying aggregate data
@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()

    # Fetch aggregation data for student marks
    cur.execute("""
    SELECT student_name,
           (dbms_marks + econometrics_marks + math_marks + calculus_marks) AS total_marks,
           (dbms_marks + econometrics_marks + math_marks + calculus_marks) / 4 AS avg_marks,
           GREATEST(dbms_marks, econometrics_marks, math_marks, calculus_marks) AS max_marks,
           LEAST(dbms_marks, econometrics_marks, math_marks, calculus_marks) AS min_marks
    FROM student_marks
    """)
    aggregation_data = cur.fetchall()

    # Get total courses count
    cur.execute("SELECT COUNT(*) FROM courses")
    total_courses = cur.fetchone()[0]

    # Get total students count
    cur.execute("SELECT COUNT(DISTINCT student_name) FROM student_marks")
    total_students = cur.fetchone()[0]

    cur.close()

    # Retrieve the user's name from the session
    name = session.get('name', 'Guest')  # Default to 'Guest' if no name found in session

    # Pass all relevant data to the template
    return render_template('dashboard.html', 
                           aggregation_data=aggregation_data,
                           total_courses=total_courses,
                           total_students=total_students,
                           name=name)


# Route for the add course page
@app.route('/addcourse', methods=['GET'])
def addcourse():
    return render_template('add_course.html')  # Render the add course form

# Route to handle form submission for adding a course
@app.route('/add_course', methods=['POST'])
def add_course():
    # Retrieve form data
    course_name = request.form['course_name']
    description = request.form['description']
    instructor = request.form['instructor']
    credits = request.form['credits']
    
    # Insert course data into the MySQL database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO courses (course_name, description, instructor, credits) VALUES (%s, %s, %s, %s)", 
                (course_name, description, instructor, credits))
    mysql.connection.commit()
    cur.close()
    
    flash('Course added successfully!', 'success')
    
    # Redirect back to the dashboard or the course list page
    return redirect(url_for('dashboard'))

# Route for the add assignment page
@app.route('/addassignment', methods=['GET'])
def addassignment():
    return render_template('add_assignment.html')  # Render the add assignment form

# Route to handle form submission for adding an assignment
@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    # Retrieve form data
    student_name = request.form['student_name']
    dbms_marks = request.form['dbms_marks']
    econometrics_marks = request.form['econometrics_marks']
    math_marks = request.form['math_marks']
    calculus_marks = request.form['calculus_marks']

    # Insert assignment data into the MySQL database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO student_marks (student_name, dbms_marks, econometrics_marks, math_marks, calculus_marks) VALUES (%s, %s, %s, %s, %s)", 
                (student_name, dbms_marks, econometrics_marks, math_marks, calculus_marks))

    mysql.connection.commit()
    cur.close()
    
    flash('Assignment added successfully!', 'success')
    
    # Redirect back to the dashboard or the assignment list page
    return redirect(url_for('dashboard'))
# Route to view grades with visualizations
@app.route('/view_grades')
def view_grades():
    cur = mysql.connection.cursor()
    
    # Fetching grades data from the database
    cur.execute("""
    SELECT student_name, dbms_marks, econometrics_marks, math_marks, calculus_marks
    FROM student_marks
    """)
    grades_data = cur.fetchall()
    cur.close()
    
    return render_template('view_grades.html', grades_data=grades_data)
@app.route('/api/grades-data')
def grades_data():
    # Assuming grades_data is a dictionary with your grades info
    return jsonify(grades_data)
@app.route('/library-resources')
def library_resources():
    cur = mysql.connection.cursor()
    
    # Execute the join query
    cur.execute("""
    SELECT 
        lr.title AS title,
        lr.author AS author,
        lr.category AS category,
        lr.availability AS availability,
        b.borrower_name AS borrower,
        bh.borrow_date AS borrow_date,
        bh.return_date AS return_date
    FROM 
        LibraryResources lr
    JOIN 
        BorrowHistory bh ON lr.resource_id = bh.resource_id
    JOIN 
        Borrowers b ON bh.borrower_id = b.borrower_id
    """)
    
    library_data = cur.fetchall()  # Fetch all joined records
    cur.close()
    return render_template('library_resources.html', library_data=library_data)
import re

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_+=<>?/|\\{}[]:;" for char in password):
        return "Password must contain at least one special character."
    return None

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        # Validate password strength
        password_error = validate_password(password)
        if password_error:
            flash(password_error, 'danger')
            return redirect(url_for('signup'))

        # Check if username or email already exists
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT * FROM signup WHERE email = %s OR username = %s
            """, (email, username))
            existing_user = cur.fetchone()
            if existing_user:
                flash('Username or email already exists. Please use a different one.', 'danger')
                cur.close()
                return redirect(url_for('signup'))
        except Exception as e:
            flash('An error occurred while checking for duplicates: ' + str(e), 'danger')
            return redirect(url_for('signup'))

        # Insert user into the database
        try:
            cur.execute("""
                INSERT INTO signup (name, email, username, password) 
                VALUES (%s, %s, %s, %s)
            """, (name, email, username, password))
            mysql.connection.commit()
            cur.close()

            flash('You successfully signed up! Please log in with your user ID and password.', 'success')
            return redirect(url_for('login'))


        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

    
    
@app.route('/announcements')
def view_announcements():
    cur = mysql.connection.cursor()

    # Get total announcements count
    cur.execute("SELECT COUNT(*) FROM announcements")
    total_announcements = cur.fetchone()[0]

    # Get unread announcements count (assuming is_new = 1 means unread)
    cur.execute("SELECT COUNT(*) FROM announcements WHERE is_new = 1")
    unread_announcements = cur.fetchone()[0]

    # Get recent announcements count (optional: announcements created in the last 30 days)
    cur.execute("SELECT COUNT(*) FROM announcements WHERE date_created >= DATE_SUB(NOW(), INTERVAL 30 DAY)")
    recent_announcements = cur.fetchone()[0]

    # Fetch all announcements, sorted by newest
    cur.execute("""
        SELECT title, message, author, date_created, is_new 
        FROM announcements 
        ORDER BY date_created DESC
    """)
    announcements = cur.fetchall()

    cur.close()

    # Render the announcements page with gathered data
    return render_template(
        'announcements.html',
        total_announcements=total_announcements,
        unread_announcements=unread_announcements,
        recent_announcements=recent_announcements,
        announcements=announcements
    )
if __name__ == '__main__':
    app.run(debug=True)

