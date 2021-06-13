from flask import Flask, render_template, url_for, redirect, session, request, flash
from flask_mysqldb import MySQL
import MySQLdb
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "2317238173128237"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "alphahacks"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)


#home
@app.route("/")
def home():
    return render_template("home.html")


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            #fetches username from 
            cursor.execute("SELECT * FROM logininfo WHERE username =%s AND password=%s ",(username,password))
            info = cursor.fetchone()
            if info is not None:
                #Checks for username and password, if not, throws exception and goes back to register page
                type = info['person_type']
                if info['username'] == username and info['password'] == password:
                    if type == "manager":
                        session['username'] = username
                        #assigns username to the session
                        return redirect(url_for("manage"))
                    else:
                        session['username'] = username
                        return redirect(url_for("signup"))
            else:
                flash("Invalid Username or Password.")
                return render_template('login.html')
    return render_template('login.html')



@app.route('/manage', methods=['GET','POST'])
def manage():
    if request.method == "GET":
        cur5 = db.connection.cursor(MySQLdb.cursors.DictCursor)
        sql_select_Query = "SELECT * from avail"
        cur5.execute(sql_select_Query)
        records = cur5.fetchall()
        #Gets all records on db
        headings = ("Name","Phone Number", "Times Available")
        data = [] 
        
        for row in records:  
            data2 = []
            #Makes 2D array storing name, number, desc, email
            data2.append(row["name"])
            data2.append(row["number"])
            data2.append(row["description"])
            data.append(data2)

        #debug       
        print(data)
    user = session.get("username", None)
    print(user)      
    return render_template('manage.html', headings = headings, data = data, username = user)
    #returns table to html file

@app.route('/about', methods=['GET'])
def about():
    if request.method == "GET":
        return render_template("about.html")
#about us page, to be done mostly in html


@app.route('/signup', methods=['GET','POST'])
def signup():
    user = session.get("username", None)
    if request.method == "POST":
        if "desc" in request.form:
            description = request.form["desc"]
            cur3 = db.connection.cursor(MySQLdb.cursors.DictCursor)
            user = session.get("username", None)
            #Starts session using username from database

            cur3.execute("SELECT * FROM logininfo WHERE username = %s",[user])
            info3 = cur3.fetchone()
            phoneNumberTemp = info3["phone_no"]
            nameTemp  = info3["name"]

            print("name: " + user)
            print(phoneNumberTemp)
            print(nameTemp)
            print(description)

            cur4 = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur4.execute("INSERT INTO login.avail(username, name, number, description)VALUES(%s,%s,%s,%s)",(user, nameTemp, phoneNumberTemp, description))
            db.connection.commit()
            flash("Time Has Been Successfully Recorded. Please enter more times or Log-Out.")
    return render_template("signup.html", username = user)


#registers user
@app.route('/new', methods=['GET', 'POST'])
def register():
    if request.method == "POST":  
        if "one" in request.form and "two" in request.form and "three" in request.form and "four" in request.form:
            name = request.form['one']
            username = request.form['two']
            password = request.form['three']
            phone_no = request.form['four']
                
            cur2 = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur2.execute("SELECT * FROM logininfo WHERE username = %s",[username])
            info2 = cur2.fetchone()

            if info2 is None:
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO login.logininfo(name, username, password, phone_no, person_type)VALUES(%s,%s,%s,%s,%s)",(name, username, password, phone_no, 'worker'))
                db.connection.commit()
                return render_template('login.html')  
            else:
                flash("Username already exists")
                return render_template('register.html')
    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug=True)