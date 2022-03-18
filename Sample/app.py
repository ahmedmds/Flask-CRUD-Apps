from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
Bootstrap(app)

# Configure DB, read from db.yaml
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    if cur.execute('INSERT INTO user VALUES(%s)', ['Mike']):
        mysql.connection.commit()
    result_value = cur.execute('SELECT * FROM user')
    if result_value > 0:
        users = cur.fetchall()
    
    seasons = ['Summer', 'Winter', 'Autumn']

    # For the input submitted in the form
    if request.method == 'POST':
        submitted_input = request.form['submitted_input']
        return 'Submitted input: ' + submitted_input, 201

    return render_template('index.html', seasons=seasons, users=users)
    # return redirect(url_for('about'))

@app.errorhandler(404)
def page_not_found(e):
    return 'This page was not found'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/css')
def css():
    return render_template('css.html') 

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Flask environment variables not used, hence debug=True for development mode, Port changed from default 5000 to 5001
