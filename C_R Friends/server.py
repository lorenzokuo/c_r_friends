from flask import Flask, render_template, session, request, redirect, flash
app = Flask(__name__)
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('friendsdb')
# now, we may invoke the query_db method
print("all the users", mysql.query_db("SELECT * FROM friends;"))

@app.route('/', methods=['GET'])
def index():
    mysql = connectToMySQL("friendsdb")
    all_friends = mysql.query_db("select * from friends")
    print("Fetched all friends", all_friends)
    if 'first_name' not in session:
        return render_template('index.html', friends = all_friends)
    return render_template("index.html", friends = all_friends, first_name = session['first_name'], last_name = session['last_name'], occupation = session['occupation'])

@app.route('/create_friend')
def create():
    mysql = connectToMySQL("friendsdb")
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
    # above %()s become the keys in the dictionary below
    # below, 'first_name' for instance, they are placeholders for the values provided in the dictionary.
    data = {
             'first_name': session['first_name'],
             'last_name':  session['last_name'],
             'occupation': session['occupation']
           }
    new_friend_id = mysql.query_db(query, data)
    # when we do an insert, we get the newly created id!
    return redirect('/')

@app.route("/process", methods=["POST"])
def checker():
    # first name
    if len(request.form['first_name']) < 1:
        flash("First name cannot be blank!", 'error')
    elif not NAME_REGEX.match(request.form['first_name']):
        flash("First name cannot contain any numbers or symbols", "error")
    elif len(request.form['first_name']) <= 3:
        flash("First name must be 3+ characters", 'error')
    # last name
    if len(request.form['last_name']) < 1:
        flash("Last name cannot be blank!", 'error')
    elif not NAME_REGEX.match(request.form['last_name']):
        flash("Last name cannot contain any numbers or symbols", "error")
    elif len(request.form['last_name']) <= 3:
        flash("Last name must be 3+ characters", 'error')
        # occupation
    if len(request.form['occupation']) < 1:
        flash("Occupation cannot be blank!", 'error')
    elif not NAME_REGEX.match(request.form['occupation']):
        flash("Occupation cannot contain any numbers or symbols", "error")
    elif len(request.form['occupation']) <= 3:
        flash("Occupation must be 3+ characters", 'error')

    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['occupation'] = request.form['occupation']

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        return redirect("/create_friend")

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
