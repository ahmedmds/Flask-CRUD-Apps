from flask import Flask, render_template, request, session, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

# Configure DB, read from db.yaml
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Random secret key generated for session data
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    # For the input submitted in the form
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            password = form['password']
            # Encrypting the password
            password = generate_password_hash(password)

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO employee(name, age, password) VALUES(%s, %s, %s)', (name, age, password))
            mysql.connection.commit()
            flash('Successfully inserted data', 'success')
        except:
            flash('Failed to insert data', 'danger')

    return render_template('index.html')

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    cur = mysql.connection.cursor()
    employees_count = cur.execute('SELECT * FROM employee')
    if employees_count > 0:
        employees = cur.fetchall()

        # The employee David (at index 0 in table) had entered password 'secret', which was encrypted at time of insertion into database
        # check_password_hash matched the fetched encrypted password (1st argument) with any given/entered string (2nd argument)
        # return str(check_password_hash(employees[0]['password'], 'secret')) # check_password_hash() returns True or False

        # Session data
        session['username'] = employees[0]['name']

        return render_template('employees.html', employees=employees)

@app.errorhandler(404)
def page_not_found(e):
    return 'This page was not found'

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Flask environment variables not used, hence debug=True for development mode, Port changed from default 5000 to 5001
