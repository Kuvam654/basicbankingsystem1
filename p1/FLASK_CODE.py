from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, flash


app = Flask(__name__, static_folder='static')
app.secret_key = b'\x0e!uAz\xed\xd2\xadeu\xb0\xa3\xae\xd0\\\xce\xb40\x7f\xd4)\xdb\\\r'

# Static files configuration
app.config['STATIC_FOLDER'] = 'static'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ABc()!?12=%'
app.config['MYSQL_DB'] = 'project1'

mysql = MySQL(app)

# Registration route
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        customerid = request.form['customerid']
        password = request.form['password']
        phonenumber = request.form['phonenumber']

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password)

        # Insert user data into MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO eeetable (customerid, password, phonenumber) VALUES (%s, %s, %s)",
                    (customerid, hashed_password, phonenumber))
        mysql.connection.commit()
        cur.close()

        # Redirect to the login route (update the route if needed)
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        customerid = request.form['customerid']
        password = request.form['password']

        # Query the database for the user
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM eeetable WHERE customerid = %s", (customerid,))
        user = cur.fetchone()
        cur.close()

        print("Entered Username:", customerid)
        print("User from database:", user)

        if user and check_password_hash(user[1], password):
            # Set user session
            session['user_id'] = customerid  # Use username as the user_id
            print("User logged in. Session user_id set to:", customerid)
            return redirect(url_for('dashboard'))

    print("Login failed. User not found or incorrect password.")
    return render_template('login.html')


# Endpoint for checking if the user is logged in
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Retrieve user information from the database
        username = session['user_id']
        cur = mysql.connection.cursor()
        
        # Replace these queries with actual queries based on your database schema
        cur.execute("SELECT bankid, bankname, bankaddress from bank where bankid = %s", (username,))
        bank = cur.fetchone()

        cur.execute("SELECT loanid, loantype, amount FROM loan WHERE customerid = %s", (username,))  # Replace ... with your conditions
        loan_data = cur.fetchone()

        '''cur.execute("SELECT branch.branchid, branch.name , branch.address FROM account JOIN branch ON account.bankid = branch.bankid JOIN bank ON branch.bankid = bank.bankid;")
        branch_data = cur.fetchhone()'''
        cur.execute("SELECT branchid, name, address FROM branch WHERE bankid = %s", (username,))  # Replace ... with your conditions
        branch_data = cur.fetchone()

        cur.execute("SELECT accountno, accounttype, balance FROM account WHERE customerid = %s", (username,))  # Replace ... with your conditions
        account_data = cur.fetchone()

        cur.execute("SELECT customerid, name, phone, address FROM customer WHERE customerid = %s", (username,))  # Replace ... with your conditions
        customer_data = cur.fetchone()

        cur.close()

        if account_data:
            # Pass user information to the template
            return render_template('bankdashboard.html',
                                   bank = bank,
                                   loan_data=loan_data,
                                   branch_data=branch_data,
                                   account_data=account_data,
                                   customer_data=customer_data)
        else:
            # Handle the case where user information is not found
            return render_template('bankdashboard.html', employee_data=None)
    else:
        return redirect(url_for('login'))

@app.route('/logout/confirm', methods=['GET', 'POST'])
def confirm_logout():
    if request.method == 'POST':
        # Placeholder logic for handling the POST request (e.g., logout)
        # Add your actual logout logic here, such as clearing the session
        # and redirecting to the login page.
        
        # Example: Clear the session
        session.clear()

        # Redirect to another page after logout (e.g., login page)
        return redirect(url_for('login'))

    else:
        # Handle the GET request (e.g., render the template)
        return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)
