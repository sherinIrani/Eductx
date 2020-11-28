from flask import Flask, render_template, request, escape, session, g, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'aakljslhbfkaljbflaksjdfbla'

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Sherin@1",
    database = "eduflask"
)

mycursor = mydb.cursor(dictionary = True)

@app.before_request 
def before_request():
    g.user = None
    if 'id' in session:
        g.user = session['id']

@app.route('/', methods = ['GET', 'POST']) 
def signin(): 
    if(request.method == 'POST'):
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        # return password
        mycursor.execute("select id, name, email, password from colleges where email = %s AND password = %s", (email, password))
        account = mycursor.fetchone()
        if account:
            session['id'] = account['id']
            message = 'Logged in successfully !'
            return render_template('dashboard.html',account=account, message=message)
        else:
            message = 'invalid'
            return render_template('collegeSignIn.html',message=message)
    else:
        return render_template('collegeSignIn.html')

@app.route('/signup', methods = ['GET', 'POST']) 
def signup():
    if(request.method == 'POST'):
        email = escape(request.form['inputEmail'])
        password = escape(request.form['inputPassword'])
        name = escape(request.form['inputName'])
        address1 = escape(request.form['inputAddress1'])
        address2 = escape(request.form['inputAddress2'])
        city = escape(request.form['inputCity'])
        state = escape(request.form['inputState'])
        pin = escape(request.form['inputZip'])
        mycursor.execute("INSERT INTO colleges (email,password,name,address1,address2,city,state,pin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (email, password, name, address1, address2, city, state, pin))
        mydb.commit()
        if mycursor.rowcount > 0:
            message = "Signup successfull. Please Login"
            return render_template('collegeSignIn.html', message=message)
        else:
            message = "Signup not successfull."
            return render_template('collegeSignup.html', message=message)    
    else:
        return render_template('collegeSignup.html')

@app.route('/dashboard') 
def dashboard():
    if g.user:
        mycursor.execute("select name from colleges where id = %s", (g.user,))
        account = mycursor.fetchone()
        return render_template('dashboard.html', account=account)
    else:
        return jsonify({"message": "please login before going to dashboard"})

@app.route('/logout') 
def logout():
    message = "Successfully Logged Out"
    session.pop('id', None)
    return render_template('collegeSignIn.html', message=message)

@app.route('/dashboard/account') 
def account():
    if g.user:
        mycursor.execute("select * from colleges where id = %s", (g.user,))
        account = mycursor.fetchall()
        return render_template('account.html', account=account)
    else:
        return jsonify({"message": "please login before going to dashboard"})

@app.route('/dashboard/createstudent', methods = ['GET','POST']) 
def cstudent():
    if g.user:
        if(request.method == 'POST'):
            uid = escape(request.form['inputUid'])
            password = escape(request.form['inputPassword'])
            name = escape(request.form['inputName'])
            batch = escape(request.form['inputBatch'])
            sem = escape(request.form['inputSem'])
            mycursor.execute("INSERT INTO students (uid,password,name,batch,sem,id) VALUES (%s, %s, %s, %s, %s, %s)", (uid, password, name, batch, sem, g.user))
            mydb.commit()
            if mycursor.rowcount > 0:
                mycursor.execute("select * from students where id = %s", (g.user,))
                account = mycursor.fetchall()
                return render_template('students.html', account=account)
            else:
                message="Student Not Created"
                return render_template('createStudent.html', message=message)
        else:
            return render_template('createStudent.html')

@app.route('/dashboard/viewstudent') 
def rstudent():
    if g.user:
        mycursor.execute("select * from students where id = %s", (g.user,))
        account = mycursor.fetchall()
        return render_template('students.html', account=account)
    else:
        return jsonify({"message": "please login before going to dashboard"})

@app.route('/dashboard/updatestudent/<uid>', methods = ['PUT']) 
def ustudent(uid):
    if g.user:
        if(request.method == 'PUT'):
            name = escape(request.form['inputName'])
            batch = escape(request.form['inputBatch'])
            sem = escape(request.form['inputSem'])
            mycursor.execute("UPDATE students SET name = %s, batch = %s, sem = %s where uid = %s", (name, batch, sem, uid))
            mydb.commit()
            if mycursor.rowcount > 0:
                return jsonify({"message":"successfull"})
            else:
                return jsonify({"message":"Not successfull"})
    else:
        return jsonify({"message": "please login before going to dashboard"})

@app.route('/dashboard/deletestudent/<uid>', methods = ['DELETE']) 
def dstudent(uid):
    if g.user:
        if(request.method == 'DELETE'):
            mycursor.execute("DELETE from students where Uid = %s AND id = %s", (uid, g.user))
            mydb.commit()
            return {"message":"Deleted"}
    else:
        return {"message": "please login before going to dashboard"}