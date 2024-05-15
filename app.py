import mysql.connector
from datetime import datetime
import random
from flask import Flask, session, render_template, redirect, url_for, request, flash

app = Flask('app')
app.secret_key = "secret_item" #we might not need this

#enter your own password here by creating a new databse
mydb = mysql.connector.connect(
    host="",
    user = "",
    password ="",
    database = "" 
)
@app.route('/', methods=['GET', 'POST'])
def login():
    mydb = mysql.connector.connect(
      host="",
      user = "",
      password ="",
      database = "" 
    )

    if request.method == 'POST':
        cursor = mydb.cursor(dictionary = True)
        id = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE uid = %s AND password = %s", (id, password,))
        account = cursor.fetchone()
        if account:
            print(account)
            session['user_type'] = account['user_type']
            session['id'] = account['uid']
        else:
           flash("wrong id or password")
    if 'user_type' not in session:
        return render_template('login.html')
    print(session['user_type'])
    if session['user_type'] == "student_ms" or session['user_type'] == "student_phd":
      cursor = mydb.cursor(dictionary = True)
      cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
      row = cursor.fetchone()
      if not row:
        cursor.execute("INSERT INTO students (s_id, Major, graduated, advisor_id) VALUES (%s, %s, %s, %s)", (session['id'], "Computer Science", "no", "90000002", ))
        mydb.commit()
    return render_template("dashboard.html")

@app.route('/newUser', methods=['POST'])
def newUser():  # Add user to DB  
  cursor = mydb.cursor(dictionary = True)  
  fname = request.form['fname'] 
  minit = request.form['minit']  
  lname = request.form['lname']  
  address = request.form['address']  
  ssn = request.form['ssn']  
  email = request.form['email'] 
  phone_no = request.form['phone_no'] 
  password = request.form['password']  
  birthday = request.form['birthday']  
  ID = ""  
  for i in range(8):   
    ID += str(random.randint(0,9))
  cursor.execute("SELECT * FROM users WHERE uid = %s", (ID,))
  row = cursor.fetchone()
  if row:
      while row:
        for i in range(8):   
          ID += str(random.randint(0,9))
        cursor.execute("SELECT * FROM users WHERE uid = %s", (ID,))
        row = cursor.fetchone()

  print("before insert")
  cursor.execute("INSERT INTO users VALUES (%s, \"applicant\", %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ID, fname, minit, lname, password, address, birthday, phone_no, ssn, email)) 
  print("before commit")
  mydb.commit()  
  print("after insert")

  yourid = "Your ID is: " + ID
  flash(yourid)
  session['id'] = ID
  session['user_type'] = 'applicant'
  return redirect('/')

#new functoinality
@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
  if "user_type" not in session:
    return redirect('/')
  rows = {}
  if request.method == "POST":
    cursor = mydb.cursor(dictionary = True)
    first_name = request.form['f_name']
    last_name = request.form['l_name']
    cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s)", ( ("%" + first_name + "%"), ("%" + last_name + "%"), ))
    rows = cursor.fetchall()
  return render_template("lookup.html", rows = rows)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if "user_type" not in session:
        return redirect('/')
    cursor = mydb.cursor(dictionary = True)
    if request.method == "POST":
        date = datetime.now()
        print(date)
        cursor.execute("INSERT INTO messages (uid, message, DATE) VALUES (%s, %s, %s)",
                                ( session['id'], request.form['message'], date,))
        mydb.commit()
        
       
    cursor.execute("SELECT messages.uid, fname, lname, message, DATE FROM messages LEFT JOIN users ON messages.uid = users.uid WHERE user_type = %s ORDER BY DATE", (session['user_type'],))
    messages = cursor.fetchall()
    return render_template("messages.html", messages = messages)

@app.route('/mail', methods=['GET', 'POST'])
def mail():
    if "user_type" not in session:
        return redirect('/')
    cursor = mydb.cursor(dictionary = True)
    error = ""
    if request.method == "POST":
        
        print(request.form['reciever'])
        cursor.execute("SELECT * FROM users WHERE uid = %s", (request.form['reciever'],))
        account = cursor.fetchone()
        if account:
           
          date = datetime.now()
          cursor.execute("INSERT INTO mail (uid, reciever, message, DATE) VALUES (%s, %s, %s, %s)", (session['id'], request.form['reciever'], request.form['message'], date,))
          mydb.commit()
          flash("Message sent successfully")
        else:
          flash("the user you are trying to send mail to does not exist")
       
    cursor.execute("SELECT fname, lname, message, DATE FROM mail LEFT JOIN users ON mail.uid = users.uid WHERE reciever = %s ORDER BY DATE DESC", (session['id'],))
    messages = cursor.fetchall()
    cursor.execute("SELECT fname, lname, message, reciever, DATE FROM mail LEFT JOIN users ON mail.uid = users.uid WHERE mail.uid = %s ORDER BY DATE DESC", (session['id'],))
    sent = cursor.fetchall()
    for i in sent:
      cursor.execute("SELECT fname, lname from users WHERE uid = %s", (i['reciever'],))
      currentuser = cursor.fetchone()
      i['fname'] = currentuser['fname']
      i['lname'] = currentuser['lname']
    return render_template("mail.html", messages = messages, error = error, sent = sent)

#ads functionality
@app.route('/advising_hold', methods=['GET', 'POST'])
def advising_hold():
    if "user_type" not in session: #error checking
        return redirect('/')
    if session['user_type'] != "student_ms":
      if session['user_type'] != "student_phd":
          return redirect('/')
    cursor = mydb.cursor(dictionary = True)
    if request.method == "POST":
        cursor.execute("DELETE FROM advising_hold WHERE student_uid = %s", (session['id'],))
        mydb.commit()
        x = 0
        for i in range(1, 13):
          cid = request.form.get(f"sid{i}")
          # print(cid)
          if cid != "":
              print(cid)
              cursor.execute("INSERT INTO advising_hold ( student_uid, cid) VALUES (%s, %s)",
                                    ( session['id'], cid,))
              mydb.commit()
              x = 1
        if x == 1:

          # cursor.execute("UPDATE students SET advising_hold = TRUE WHERE s_id = %s", (session['id'],))
          # mydb.commit()
          cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
          advisor = cursor.fetchone()
          r = advisor['advisor_id']
          cursor.execute("SELECT fname, lname FROM users WHERE uid = %s", (r,))
          advisor = cursor.fetchone()
          advisor = advisor['fname'] + " " + advisor['lname']
          flash("advising hold submitted successfully contact your advisor " + advisor + " to approve it")

       
    cursor.execute("SELECT * from classes")
    courses = cursor.fetchall()
    cursor.execute("SELECT s_id, fname, lname from students INNER JOIN users ON s_id = uid WHERE s_id = %s", (session['id'],))
    id = session['id']
    rows = cursor.fetchall()
    return render_template("advising_hold.html", courses = courses, rows = rows, id = id)

@app.route('/approve_advising_hold', methods=['GET', 'POST'])
def approve_advising_hold():
    if "user_type" not in session: #error checking
        return redirect('/')
    if session['user_type'] != "faculty":
       return redirect('/')
    cursor = mydb.cursor(dictionary = True)
    if request.method == "POST" and "final" in request.form:
        final = request.form['final']
        if final == "True":
            cursor.execute("UPDATE students SET advising_hold = %s WHERE s_id = %s", (True, request.form['sx_id'],))
            mydb.commit()
            flash("advising hold approved successfully")
        else:
           flash("advising form rejected")
        cursor.execute("DELETE FROM advising_hold WHERE student_uid = %s", ( request.form['sx_id'],))
        mydb.commit()

        return redirect('/Faculty_Approve_Thesis')
    if request.method == "POST" and "sx_id" in request.form:
        
        s_id = request.form['sx_id']
        print(s_id)
        cursor.execute("SELECT advising_hold.cid, class_number, dept, title FROM advising_hold INNER JOIN classes ON advising_hold.cid = classes.cid WHERE student_uid = %s", (s_id ,))
        rows = cursor.fetchall()
        r = len(rows)
        return render_template("approve_advising_hold.html", rows = rows, r= r, s_id = s_id)
    return redirect('/')


@app.route('/GS_queries', methods=['GET', 'POST'])
def GS_queries():
    if "user_type" not in session: #error checking
        return redirect('/')
    if session['user_type'] != "admin":
      if session['user_type'] != "GS":
        return redirect('/')
    cursor = mydb.cursor(dictionary = True)
    if request.method == "POST":
        graduation = request.form['graduation_year']
        fname = request.form['f_name']
        lname = request.form['l_name']
        s_id = request.form['s_id']
        if graduation == "":
            cursor.execute("SELECT uid, user_type, fname, lname,email, graduation_year FROM users INNER JOIN students ON s_id = uid WHERE (user_type = %s OR user_type = %s or user_type = %s) AND (uid LIKE (%s) AND fname LIKE (%s) AND lname LIKE (%s) )", ("student_ms", "student_phd", "alumni", ("%" + s_id + "%"), ("%" + fname + "%"), ("%" + lname + "%"), ))
            rows = cursor.fetchall()
        else:
            cursor.execute("SELECT uid, user_type, fname, lname,email, graduation_year FROM users INNER JOIN students ON s_id = uid WHERE (user_type = %s OR user_type = %s or user_type = %s) AND (uid LIKE (%s) AND fname LIKE (%s) AND lname LIKE (%s) AND graduation_year LIKE (%s) )", ("student_ms", "student_phd", "alumni", ("%" + s_id + "%"), ("%" + fname + "%"), ("%" + lname + "%"), ("%" + graduation + "%"),))
            rows = cursor.fetchall()

        return render_template('GS_queries.html', rows = rows)


    cursor.execute("SELECT uid, user_type, fname, lname,email, graduation_year FROM users INNER JOIN students ON s_id = uid WHERE user_type = %s OR user_type = %s or user_type = %s", ("student_ms", "student_phd", "alumni",))
    rows = cursor.fetchall()
    print(rows)
    
    return render_template('GS_queries.html', rows = rows)

@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if "user_type" not in session: #error checking
        return redirect('/')
    if session['user_type'] != "student_ms":
      if session['user_type'] != "student_phd":
          return redirect('/')
    fail = 1
    if request.method == "POST" and "submit" in request.form:
        n = 1
        checkdup = 0#checks if there is a duplicate
        cursor = mydb.cursor(dictionary = True)
        cursor.execute("DELETE FROM form1 WHERE student_uid = %s", (session['id'],))
        cursor.execute("UPDATE students SET form1 = FALSE WHERE s_id = %s", (session['id'],))
        mydb.commit()
        for i in range(1, 13):
            checkdup = 0#checks if there is a duplicate
            fail = 0
            cursor.execute("SELECT * FROM form1 WHERE student_uid = %s", (session['id'],))
            classes = cursor.fetchall()
            cid = request.form.get(f"sid{i}")
            for i in classes:
                if i['cid'] == cid:
                    # print("duplicate")
                    checkdup = 1
                    n =1
                    fail = 1
                    flash("form not working because of duplicate classes inserted")
                    break

            cursor.execute("SELECT * FROM classes")
            courses = cursor.fetchall()
            if (checkdup == 0):
                for i in courses:
                    
                    if i['cid'] == cid:
                        n = 0 
                        cursor.execute("INSERT INTO form1 ( student_uid, cid) VALUES (%s, %s)",
                                ( session['id'], cid,))
                # Only add from the fields that were filled out
            
        if n == 0:
            
            mydb.commit()
            cursor.execute("SELECT * FROM form1 where student_uid = %s", (session['id'],))
            tester = cursor.fetchall()
            cursor.execute("SELECT * FROM enrollment WHERE student_uid = %s", (session['id'],))
            rows = cursor.fetchall()
            checker = 1
            if session['user_type'] == "student_ms":
                gpa = 0
                credit = 0
                TC = 0#gets the total credit of non in progress classes
                core = 0
                notcs = 0
                k = 0#check if there is a class planned
                n =0
                for i in tester:
                    cursor.execute("SELECT * FROM classes WHERE cid = %s", (i['cid'],))
                    row = cursor.fetchone()
                    credit = int(row['credit_hours'])
                    TC+=credit
                    if row['dept'] != "CSCI":
                        notcs+=1
                    if (row['dept'] == "CSCI"):
                        if (row["class_number"] == 6212 or row["class_number"] == 6221 or row["class_number"] == 6461):
                          core+=1
                if TC < 30:
                    flash("the total credit is less than 30")
                    fail = 1
                if notcs >2:
                    flash("you listed more than 2 not cs classes")
                    fail = 1
                if core != 3:
                    flash("you did not list all 3 core classes")
                    fail = 1
                for i in tester:
                    checker = 0
                    for j in rows:
                        if j['cid'] == i['cid']:
                            if j['grade'] == "IP":
                                cursor.execute("SELECT * FROM classes WHERE cid = %s", (j['cid'],))
                                row = cursor.fetchone()
                                string = "failed because " + (row['dept'])+ " " + str(row['class_number']) + " is an in progress classes"
                                flash(string)
                                fail = 1
                            checker = 1
                            
                    if (checker == 0):#then there is a class in form1 that is not in enrollments
                        cursor.execute("SELECT * FROM classes WHERE cid = %s", (i['cid'],))
                        row = cursor.fetchone()
                        string = "failed because you did not take " + str(row['dept']) + " "  + str(row['class_number'])
                        flash(string)
                        checker = 0
                        break
                    
                if (checker == 0):
                    fail = 1
                
                if (fail == 0):
                    flash("form 1 submitted successfully")
                    cursor.execute("UPDATE students SET form1 = TRUE WHERE s_id = %s", (session['id'],))
                    mydb.commit()
            
            if session['user_type'] == "student_phd":
                gpa = 0
                credit = 0
                TC = 0#gets the total credit of non in progress classes
                core = 0
                cscredit = 0
                k = 0#check if there is a class planned
                n =0
                for i in tester:
                    cursor.execute("SELECT * FROM classes WHERE cid = %s", (i['cid'],))
                    row = cursor.fetchone()
                    credit = int(row['credit_hours'])
                    TC+=credit
                    if row['dept'] == "CSCI":
                        cscredit+=credit
                    
                    
                if TC < 36:
                    flash("the total credit is less than 36")
                    fail = 1
                if cscredit < 30:
                    flash("your CS credit should be more than or 30")
                    fail = 1
                
                
                for i in tester:
                    print(i['cid'])
                    checker = 0
                    for j in rows:
                        if j['cid'] == i['cid']:
                            if j['grade'] == "IP":
                                cursor.execute("SELECT * FROM classes WHERE cid = %s", (j['cid'],))
                                row = cursor.fetchone()
                                string = "failed because " + (row['dept'])+ " " + str(row['class_number']) + " is an in progress classes"
                                flash(string)
                                fail = 1
                            checker = 1
                    if (checker == 0):#then there is a class in enrollments that is not in form1
                        cursor.execute("SELECT * FROM classes WHERE cid = %s", (i['cid'],))
                        row = cursor.fetchone()
                        string = "failed because you did not take " + str(row['dept']) + " "  + str(row['class_number'])
                        flash(string)
                        checker = 0
                        break
                if (checker == 0):
                    fail = 1
                
                if (fail == 0):
                    flash("form 1 submitted successfully")
                    cursor.execute("UPDATE students SET form1 = TRUE WHERE s_id = %s", (session['id'],))
                    mydb.commit()

        cursor.close()

    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT s_id, fname, lname from students INNER JOIN users ON s_id = uid WHERE s_id = %s", (session['id'],))
    id = session['id']
    rows = cursor.fetchall()

    cursor.execute("SELECT * from classes")
    courses = cursor.fetchall()
    # print(courses)
    return render_template("form1.html", id = id, rows = rows, courses = courses)

@app.route('/Student_Advising', methods=['GET', 'POST'])
def studentavising():
    if "user_type" not in session: #error checking
        return redirect('/')
    if session["user_type"] == "student_ms" or session["user_type"] == "student_phd":
      cursor = mydb.cursor(dictionary = True)
      cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
      row = cursor.fetchone()
      if not row:
        cursor.execute("INSERT INTO students (s_id, Major, graduated, advisor_id) VALUES (%s, %s, %s, %s)", (session['id'], "Computer Science", "no", "90000002", ))
        mydb.commit()
      return render_template("Student_Advising.html")
    return redirect('/')

@app.route('/Editinfo', methods=['GET', 'POST'])
def Editinfo():
    if "user_type" not in session: #error checking
      return redirect('/')
    message = ""
    cursor = mydb.cursor(dictionary = True)
    if request.method == "POST":
        cursor.execute("SELECT * FROM users where email = %s AND uid != %s", (request.form['my_email'], session['id'],))
        info = cursor.fetchone()
        if info:
            flash("email already exists")
        else:
          cursor.execute("UPDATE users SET email = %s, password = %s, address = %s, phone_no = %s, fname = %s, minit = %s, lname = %s, birthday = %s WHERE uid = %s", 
                         (request.form['my_email'], request.form['my_password'], request.form['my_address'], request.form['my_phone_no'], request.form['my_fname'], request.form['my_minit'], request.form['my_lname'], request.form['my_birthday'], session['id'],))
          mydb.commit()
          flash("information updated successfully")

    cursor.execute("SELECT * FROM users where uid = %s", (session['id'],))
    info = cursor.fetchone()
    return render_template("Editinfo.html", info = info)

@app.route('/view_form1', methods=['GET', 'POST'])
def viewform1():
    if "user_type" in session:
        if request.method == "POST":
            cursor = mydb.cursor(dictionary = True) 
            s_id = request.form['student_id']
            print(s_id)
            cursor.execute("SELECT form1.cid, class_number, dept, title FROM form1 INNER JOIN classes ON form1.cid = classes.cid WHERE student_uid = %s", (s_id ,))
            rows = cursor.fetchall()
            r = len(rows)
            return render_template("view_form1.html", rows = rows, r =r , s_id = s_id)
    return redirect('/')

#this function is for the requirements for both masters and phd students
@app.route('/Graduation_Requirements', methods=['GET', 'POST'])
def Graduation_Requirements():
    cursor = mydb.cursor(dictionary = True)

    if "user_type" not in session: #error checking
        return redirect('/')
    if session["user_type"] == "student_ms":
        
        n = 0
        cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
        row = cursor.fetchone()
        form1 = row['form1']
        if form1 == 1:
            form1 = True
        else:
            form1 = False
        dicts = requirement(session['id'])
        dicts["form1"] =  form1
        print(dicts['gpa'])
        if dicts["counter"] <= 2 and dicts["gpa"] >= 3 and dicts['tc'] >= 30 and dicts["core"] == 3 and dicts["form1"] == True:
            if request.method == "POST":# here is where i check if someone submits the graduate 
                cursor.execute("UPDATE students SET graduated = %s WHERE s_id = %s", ("pending",session['id'],))
                mydb.commit()
                flash("your applicatoin is currently pending the GS will look into it")
                return render_template("Student_Advising.html")
            n = 1
        if n == 1:
           flash("You can graduate")
        else:
           flash("You can't graduate")
        return render_template("Graduation_Requirements.html", req = dicts, n = n)
    if session["user_type"] == "student_phd":
        n = 0 #checks wether or not a student can graduate
        cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
        row = cursor.fetchone()
        form1 = row['form1']
        if form1 == 1:
            form1 = True
        else:
            form1 = False
        thesis = row['thesis']
        dicts = requirement(session['id'])
        dicts["thesis"] = thesis
        dicts["form1"] =  form1
        if dicts["counter"] <= 1 and dicts["gpa"] >= 3.5 and dicts['tc'] >= 36 and dicts["cscredit"] >=30 and dicts["form1"] == True and dicts['thesis'] == "approved":
            if request.method == "POST":# here is where i check if someone submits the graduate 
                cursor.execute("UPDATE students SET graduated = %s WHERE s_id = %s", ("pending",session['id'],))
                mydb.commit()
                flash("your applicatoin is currently pending the GS will look into it")
                return render_template("Student_Advising.html")
            n = 1
            
        if n == 1:
           flash("You can graduate")
        else:
           flash("You can't graduate")
        return render_template("Graduation_Requirements.html",  req = dicts, n = n)
    return redirect('/')
# this is just for the phd student
#its a function that updates the database whenever the students submits it
@app.route('/Thesis', methods=['GET', 'POST'])
def Thesis():
    cursor = mydb.cursor(dictionary = True)

    if "user_type" not in session: #error checking
        return redirect('/')
    if session["user_type"] == "student_phd" or session["user_type"] == "student_ms":
      if request.method == "POST":
            cursor.execute("UPDATE students SET thesis = %s, thesis_text = %s WHERE s_id = %s", ("pending", request.form['thesis'], session['id'],))
            mydb.commit()
            cursor.execute("SELECT * FROM students where s_id = %s", (session['id'],))
            row = cursor.fetchone()
            cursor.execute("SELECT * FROM users where uid = %s", (row['advisor_id'],))
            advisor = cursor.fetchone()
            advisor = advisor['fname'] + " " + advisor['lname']
            submitted = "your advisor " + advisor + " has received your thesis and will look into it"
            flash(submitted)
            return render_template("Thesis.html" )
      return render_template("Thesis.html")
    return redirect('/')

def requirement(id):
    mydict = {}
    gpa = 0
    credit = 0
    TC = 0
    core = 0
    notcs = 0
    counter = 0
    n =0
    cscredit = 0
    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT * FROM enrollment WHERE student_uid = %s", (id,))
    rows = cursor.fetchall()

    if rows:
            for i in rows:
                cursor.execute("SELECT * FROM classes WHERE cid = %s", (i['cid'],))
                row = cursor.fetchone()
                if(i['grade'] == "IP"):#doesnt count IP CLASSES
                    k = 1
                else:
                    credit = int(row['credit_hours'])
                    TC+=credit
                    if row['dept'] != "CSCI":
                        notcs+=1
                    else:
                        cscredit+=credit
                    if (row['dept'] == "CSCI"):
                        if (row["class_number"] == 6212 or row["class_number"] == 6221 or row["class_number"] == 6461):
                            core+=1
                    gpa += getGPA(i['grade']) * credit
                    if(getGPA(i['grade']) < 3):
                        counter+=1
            if TC == 0:
                gpa = 0
            else:
                gpa/=TC
    mydict ={"gpa": gpa, "tc": TC, "counter":counter, "core":core, "notcs": notcs, "cscredit": cscredit}
    return mydict

def getGPA(courseLetterGrade):
    if (courseLetterGrade == "A"):
        return 4.0;
    elif (courseLetterGrade == "A-"):
        return 3.7
    elif (courseLetterGrade == "B+"):
        return 3.3
    elif (courseLetterGrade == "B"):
        return 3.0;
    elif (courseLetterGrade == "B-"):
        return 2.7
    elif (courseLetterGrade == "C+"):
        return 2.3
    elif (courseLetterGrade == "C"):
        return 2.0;
    elif (courseLetterGrade == "D"):
        return 1.0;
    elif (courseLetterGrade == "F"):
        return 0
    else:
        return "IP"

#this route is for the GS to approve the students who are ready to graduate
@app.route('/GS_Approve_Students', methods=['GET', 'POST'])
def GS_Approve_Students():
    if "user_type" not in session: #error checking
        return redirect('/')

    if session["user_type"] == "GS" or session["user_type"] == "admin":
        cursor = mydb.cursor(dictionary = True)
        if request.method == "POST" and "currid" in request.form: #approving graduation
            today = datetime.today()
            year = today.year
            cursor.execute("UPDATE students SET graduated = %s , graduation_year = %s WHERE s_id = %s", ("yes", year, request.form['currid'], ))
            mydb.commit()
            cursor.execute("UPDATE users SET user_type = %s WHERE uid = %s", ("alumni", request.form['currid'],))
            mydb.commit()
            flash("Student graduated 🎉🎉")
        #changing advisors
        if request.method == "POST" and "search_id" in request.form:
            new_id = request.form['search_id']
            cursor.execute("SELECT s_id, Major, user_type, fname, minit, lname, thesis FROM students INNER JOIN users ON s_id = uid WHERE graduated = %s AND s_id LIKE %s", ("pending", ("%" + new_id + "%"),))
            pending = cursor.fetchall()
            
            cursor.execute("SELECT * FROM users WHERE user_type = %s", ("faculty",))
            advisors = cursor.fetchall()

            session['majors'] = ['Computer Science', 'Mathematics', 'Electrical and Computer Engineering']

            cursor.execute("SELECT s_id, Major, thesis, fname, minit, lname, user_type, advisor_id FROM students JOIN users ON s_id = uid WHERE (graduated != %s OR user_type != %s) AND s_id LIKE %s", ("yes","alumni",("%" + new_id + "%"),))
            students = cursor.fetchall()
            return render_template("GS_Approve_Students.html", pending = pending, advisors = advisors, students = students)

        if request.method == "POST" and "newadvisor" in request.form:
            
            cursor.execute("UPDATE students SET advisor_id = %s WHERE s_id = %s", (request.form['newadvisor'], request.form['s_id'],))
            mydb.commit()
            flash("advisor changed successfully")

        if request.method == "POST" and "new_major" in request.form:
            
            cursor.execute("UPDATE students SET Major = %s WHERE s_id = %s", (request.form['new_major'], request.form['s_id'],))
            mydb.commit()
            flash("major changed successfully")
        cursor.execute("SELECT s_id, Major, user_type, fname, minit, lname, thesis FROM students INNER JOIN users ON s_id = uid WHERE graduated = %s", ("pending",))
        pending = cursor.fetchall()
        
        cursor.execute("SELECT * FROM users WHERE user_type = %s", ("faculty",))
        advisors = cursor.fetchall()

        session['majors'] = ['Computer Science', 'Mathematics', 'Electrical and Computer Engineering']

        cursor.execute("SELECT s_id, Major, thesis, fname, minit, lname, user_type, advisor_id FROM students JOIN users ON s_id = uid WHERE graduated != %s OR user_type != %s", ("yes","alumni",))
        students = cursor.fetchall()
        return render_template("GS_Approve_Students.html", pending = pending, advisors = advisors, students = students)
    return redirect('/')

@app.route('/Faculty_Approve_Thesis', methods=['GET', 'POST'])
def Faculty_Approve_Thesis():
    if "user_type" not in session:
        return redirect('/')
    if session['user_type'] == "faculty":
            cursor = mydb.cursor(dictionary = True) 
            if request.method == "POST":
                s_id = request.form['student_id']
                cursor.execute("UPDATE students SET thesis = %s WHERE s_id = %s", (request.form['check'],s_id ,))
                mydb.commit()
                if request.form['check'] == "approved":
                   flash("Thesis approved")
                else:
                   flash("Thesis rejected")
            cursor.execute("SELECT s_id, fname, minit, lname  FROM students INNER JOIN users On s_id = uid WHERE advisor_id = %s", (session['id'],))
            rows = cursor.fetchall()
            cursor.execute("SELECT s_id, fname, minit, lname, thesis_text FROM students INNER JOIN users On s_id = uid where advisor_id = %s AND thesis = %s", (session['id'],"pending", ))
            pending = cursor.fetchall()
            
            return render_template("Faculty_Approve_Thesis.html", rows = rows, pending = pending)
    return redirect('/')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def prereq_check(section_id):
  cursor = mydb.cursor(dictionary=True)

  cursor.execute('''
  SELECT sections.cid, class_number, day, timeslot 
  FROM sections 
    JOIN classes ON sections.cid = classes.cid 
  WHERE sections.section_id = %s''',
                 (section_id, ))
  course = cursor.fetchone()

  eligable = True
  cursor.execute('SELECT prereq_cid AS cid FROM prereqs WHERE class_cid = %s', 
                 (course['cid'], ))
  prereqs = cursor.fetchall()

  cursor.execute('SELECT cid FROM enrollment WHERE student_uid = %s and finalized = 1', 
                 (session['id'], ))
  courses_taken = cursor.fetchall()

  for prereq in prereqs:
    if prereq not in courses_taken:
      eligable = False
          
  if session['user_type'] == 'student_phd' and int(course['class_number']) < 6000:
    eligable = False

  cursor.execute('''
  SELECT sections.section_id, sections.day, sections.timeslot, sections.cid 
  FROM sections 
    JOIN classes ON classes.cid = sections.cid 
    JOIN enrollment ON enrollment.section_id = sections.section_id
  WHERE sections.year = %s 
    AND sections.semester = %s 
    AND enrollment.student_uid = %s''', 
                 (str(session['current_year']), str(session['current_semester']), session["id"],))
  current_classes = cursor.fetchall()

  for c in current_classes:
    if c['day'] == course['day'] and abs(c['timeslot'] - course['timeslot']) != 2:
      eligable = False
    elif c['cid'] == course['cid']:
      eligable = False

  return eligable

def classes_search(department = "%", title = "%", class_number = "%"):
  cursor = mydb.cursor(dictionary=True)

  cursor.execute('''
  SELECT * 
  FROM sections 
    JOIN classes ON classes.cid = sections.cid 
    JOIN users ON users.uid = sections.professor_uid
  WHERE sections.year = %s 
    AND sections.semester = %s 
    AND classes.dept LIKE (%s) 
    AND classes.title LIKE (%s) 
    AND classes.class_number LIKE (%s)''',
                 (str(session['current_year']), str(session['current_semester']), department, title, class_number))
  all_classes = cursor.fetchall()

  cursor.execute('''
  SELECT sections.section_id 
  FROM sections 
    JOIN classes ON classes.cid = sections.cid 
    JOIN users ON users.uid = sections.professor_uid
    JOIN enrollment ON enrollment.section_id = sections.section_id
  WHERE sections.year = %s 
    AND sections.semester = %s 
    AND enrollment.student_uid = %s''', 
                 (str(session['current_year']), str(session['current_semester']), session["id"],))
  current_classes = cursor.fetchall()

  session['lookup_results_classes'] = []
  for course in all_classes:
    if {'section_id': course['section_id']} not in current_classes:
      course['eligable'] = prereq_check(course['section_id'])
      session['lookup_results_classes'].append(course)

# Student regestration page
@app.route('/student_regestration', methods = ['GET', 'POST'])
def student_regestration():
  cursor = mydb.cursor(dictionary=True)
  # doesn't allow access if not logged in as student
  if session["user_type"] != "student_phd" and session['user_type'] != 'student_ms':
    return redirect(url_for("logout"))
  cursor.execute("SELECT * FROM students WHERE s_id = %s", (session['id'],))
  r = cursor.fetchone()
  if r['advising_hold'] == False:
     flash("Advising form must be approved before regiestration")
     return redirect('/')
  # set up for schedule
  session['years'] = [2023, 2024]
  session['semesters'] = ['spring', 'summer', 'fall']
  session['student_regestration_error'] = ''
  if 'current_year' not in session:
    session['current_year'] = 2023
  if 'current_semester' not in session:
    session['current_semester'] = 'fall'
  session['semester_names'] = ['blank', 'spring', 'summer', 'fall'] # 'blank' because there is no 0 semester
  session['different_periods'] = ['3-5:30pm', '4-6:30pm', '6-8:30pm']
  session['different_periods_2'] = ['blank', '3-5:30pm', '4-6:30pm', '6-8:30pm'] # 'blank' because there is no 0 timeslot

  # Make the original schedule
  if 'schedule' not in session:
    session['schedule'] = []
    cursor.execute('''
    SELECT * 
    FROM enrollment JOIN classes ON classes.cid = enrollment.cid 
        JOIN sections ON enrollment.section_id = sections.section_id 
    WHERE enrollment.student_uid = %s 
        AND sections.year = %s 
        AND sections.semester = %s''',
                    (session['id'], str(session['current_year']), str(session['current_semester'])))
    classes_taking = cursor.fetchall()

    days = ['M', 'T', 'W', 'R', 'F']
    session['schedule'] = [[['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']]]
    for course in classes_taking:
      session['schedule'][course['timeslot'] - 1][days.index(course['day'])] = [course['title'], course['section_id']]


  # Make the original class search list
  classes_search()

  # Allows users to search for classes
  if request.method == 'POST' and 'class_lookup' in request.form:
    department = '%'
    title = '%'
    number = '%'

    if request.form['department'] != '':
      department = request.form['department']
    if request.form['title'] != '':
      title = request.form['title']
    if request.form['number'] != '':
      number = request.form['number']
    
    classes_search(department, title, number)
  
  # Allow users to pick the semester they want to see their schedule for
  elif request.method == 'POST' and 'semester' in request.form:
    session['current_semester'] = str(request.form['semester'])
    session['current_year'] = int(request.form['year'])
    
    classes_search()

    # get all classes from database for that semester/year
    session['schedule'] = []
    cursor.execute('''
    SELECT * 
    FROM enrollment JOIN classes ON classes.cid = enrollment.cid 
        JOIN sections ON enrollment.section_id = sections.section_id 
    WHERE enrollment.student_uid = %s 
        AND sections.year = %s 
        AND sections.semester = %s''',
                    (session['id'], str(session['current_year']), str(session['current_semester'])))
    classes_taking = cursor.fetchall()
    days = ['M', 'T', 'W', 'R', 'F']
    session['schedule'] = [[['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']]]
    for course in classes_taking:
      session['schedule'][course['timeslot'] - 1][days.index(course['day'])] = [course['title'], course['section_id']]

  elif request.method == 'POST':
    cursor.execute('''
    SELECT sections.section_id, classes.title, enrollment.finalized, sections.timeslot, sections.day, sections.cid
    FROM sections 
      LEFT JOIN classes ON classes.cid = sections.cid 
      LEFT JOIN users ON users.uid = sections.professor_uid
      LEFT JOIN enrollment ON enrollment.section_id = sections.section_id
    WHERE sections.year = %s 
      AND sections.semester = %s ''',
                   (str(session['current_year']), str(session['current_semester'])))
    all_classes = cursor.fetchall()

    cursor.execute('''
    SELECT sections.section_id 
    FROM sections 
      JOIN classes ON classes.cid = sections.cid 
      JOIN users ON users.uid = sections.professor_uid
      LEFT JOIN enrollment ON enrollment.section_id = sections.section_id
    WHERE sections.year = %s 
      AND sections.semester = %s 
      AND enrollment.student_uid = %s''', 
                   (str(session['current_year']), str(session['current_semester']), session["id"],))
    current_classes = cursor.fetchall()

    for course in all_classes:
      # drop
      if {'section_id': course['section_id']} in current_classes and course['title'] in request.form:
        if course['finalized'] == 0:
            session['schedule'][course['timeslot'] - 1][['M', 'T', 'W', 'R', 'F'].index(course['day'])] = ['free period', 'none']
            cursor.execute('DELETE FROM enrollment WHERE enrollment.student_uid = %s AND enrollment.section_id = %s',
                          (session['id'], course['section_id']))
            mydb.commit()
        else:
          session['student_regestration_error'] = 'can not drop a finalized class'
      # add
      elif course['title'] in request.form and prereq_check(course['section_id']):
        session['schedule'][course['timeslot'] - 1][['M', 'T', 'W', 'R', 'F'].index(course['day'])] = [course['title'], course['section_id']]
        cursor.execute('INSERT INTO enrollment VALUE(%s, %s, %s, %s, %s)',
                      (session['id'], course['cid'], course['section_id'], 'IP', 0))
        mydb.commit()
    
    classes_search()
  
  return render_template('student_regestration.html')

# faculty regestration page
@app.route('/faculty_regestration', methods = ['GET', 'POST'])
def faculty_regestration():
  cursor = mydb.cursor(dictionary=True)

  # doesn't allow access if not logged in as faculty
  if session["user_type"] != "faculty":
    return redirect(url_for("logout"))

  session['years'] = [2023, 2024]
  session['semesters'] = ['spring', 'summer', 'fall']
  session['faculty_regestration_error'] = ''
  if 'current_year' not in session:
    session['current_year'] = 2023
  if 'current_semester' not in session:
    session['current_semester'] = 'fall'
  session['semester_names'] = ['blank', 'spring', 'summer', 'fall'] # 'blank' becaues there is no 0 semester
  session['different_periods'] = ['3-5:30pm', '4-6:30pm', '6-8:30pm']
  session['different_periods_2'] = ['blank', '3-5:30pm', '4-6:30pm', '6-8:30pm']

  # Make the blank schedule
  if 'schedule' not in session:
    session['schedule'] = []
    cursor.execute('''
    SELECT * 
    FROM sections 
        JOIN classes ON classes.cid = sections.cid 
        JOIN users ON sections.professor_uid = users.uid 
    WHERE users.uid = %s 
        AND sections.year = %s 
        AND sections.semester = %s''',
                    (session['id'], str(session['current_year']), str(session['current_semester'])))
    classes_teaching = cursor.fetchall()

    days = ['M', 'T', 'W', 'R', 'F']
    session['schedule'] = [[['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']]]
    for course in classes_teaching: 
      session['schedule'][course['timeslot'] - 1][days.index(course['day'])] = [course['title'], course['section_id']]
  
  # Allow users to pick the semester they want to see there schedule for
  if request.method == 'POST' and 'semester' in request.form:
    session['current_semester'] = str(request.form['semester'])
    session['current_year'] = int(request.form['year'])

    session['schedule'] = []
    cursor.execute('''
    SELECT * 
    FROM sections 
        JOIN classes ON classes.cid = sections.cid 
        JOIN users ON sections.professor_uid = users.uid 
    WHERE users.uid = %s 
        AND sections.year = %s 
        AND sections.semester = %s''',
                    (session['id'], str(session['current_year']), str(session['current_semester'])))
    classes_teaching = cursor.fetchall()
    days = ['M', 'T', 'W', 'R', 'F']
    session['schedule'] = [[['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']], [['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none'], ['free period', 'none']]]
    for course in classes_teaching: 
      session['schedule'][course['timeslot'] - 1][days.index(course['day'])] = [course['title'], course['section_id']]
  
  return render_template('faculty_regestration.html')

@app.route("/sysadmin/<id>", methods = ["GET", "POST"])
def sysadmin_id(id):
  cursor = mydb.cursor(dictionary = True)
  if ("user_type") not in session:
    return redirect('/')
  if session['user_type'] != "admin":
    return redirect('/')
  if request.method == 'POST':
      fn = request.form["first_name"]
      mi = request.form["middle_initial"]
      ln = request.form["last_name"]
      ad = request.form["address"]
      ut = request.form["user_type"]
      print(ut)
      bd = request.form["birthday"]
      phone_no = request.form["phone_no"]
      ssn = request.form["ssn"]
      email = request.form["email"]
      cursor.execute("UPDATE users SET fname = (%s), minit = (%s), lname = (%s), address = (%s), birthday = (%s), phone_no = (%s), ssn = (%s), email = (%s),  user_type = (%s) WHERE uid = (%s)", 
                    (fn, mi, ln, ad, bd, phone_no, ssn, email, ut, id, ))
      mydb.commit()
      flash("user info changed successfully")
      return redirect('/sysadmin_regestration')
  cursor.execute("SELECT * FROM users WHERE uid = %s", (id, ))
  user = cursor.fetchone()
  types = ["applicant", "student_ms", "student_phd", "alumni", "faculty", "reviewer", "GS", "CAC", "admin"]
  
  return render_template("sysadmin_id.html", user = user , types = types)
# system admin regestration
@app.route("/sysadmin_regestration", methods = ["GET", "POST"])
def sysadmin_regestration():
  cursor = mydb.cursor(dictionary = True)
  if "error" not in session:
    session["error"] = ""
  session["error"] = ""
  
  # redirects to login if user not sysadmin
  if session["user_type"] != "admin":
    return redirect(url_for("logout"))

  first_name = "%"
  last_name = "%"
  uid = "%"
  user_type = "%"

  # build users list
  cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s) and uid LIKE (%s) and user_type LIKE (%s)", (first_name, last_name, uid, user_type))
  lookup_results = cursor.fetchall()
  session["sysadmin_Lookup_Results"] = []
  for student in lookup_results:
    session["sysadmin_Lookup_Results"].append(student)
    # print(student)
  
  session['possible_user_types'] = ["applicant", "student_ms", "student_phd", "alumni", "faculty", "reviewer", "GS", "CAC", "admin"]

  if request.method == 'POST':
    if request.form["Form_Type"] == "search":
      first_name = "%"
      last_name = "%"
      uid = "%"
      user_type = "%"

      if request.form['first_name'] != '':
        first_name = request.form['first_name']
      if request.form['last_name'] != '':
        last_name = request.form['last_name']
      if request.form['uid'] != '':
        uid = request.form['uid']
      if request.form['user_type'] != "":
        user_type = request.form["user_type"]
    
      # build users list
      cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s) and uid LIKE (%s) and user_type LIKE (%s)", (first_name, last_name, uid, user_type))
      lookup_results = cursor.fetchall()
      session["sysadmin_Lookup_Results"] = []
      for student in lookup_results:
        session["sysadmin_Lookup_Results"].append(student)
    
    elif request.form["Form_Type"] == "add user":
      uid = request.form["uid"]
      cursor.execute("SELECT uid FROM users")
      all_users = cursor.fetchall()
      error = False
      for user in all_users:
        if str(user["uid"]) == uid:
          error = True
          flash("uid already taken")
          if "error" not in session:
            session["error"] = "uid already taken"
          session["error"] = "uid already taken"

      fn = request.form["fname"]
      mi = request.form["minit"]
      ln = request.form["lname"]
      ad = request.form["address"]
      bd = request.form["birthday"]
      phone_no = request.form["phone_no"]
      ssn = request.form["ssn"]
      email = request.form["email"]
      ut = request.form["user_type"]
      pw = "pass"

      # TODO: display error
      if error == False:
        cursor.execute("INSERT INTO users (uid, password, fname, minit, lname, address, birthday, phone_no, ssn, email, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (uid, pw, fn, mi, ln, ad, bd, phone_no, ssn, email, ut))
        mydb.commit()
        flash("user added successfully")
        if "error" not in session:
          session["error"] = "uid already taken"
        session["error"] = ""
      # build users list
      cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s) and uid LIKE (%s) and user_type LIKE (%s)", (first_name, last_name, uid, user_type))
      lookup_results = cursor.fetchall()
      session["sysadmin_Lookup_Results"] = []
      for student in lookup_results:
        session["sysadmin_Lookup_Results"].append(student)
      return redirect('/sysadmin_regestration')
    
    elif request.form["Form_Type"] == "delete user":
      cursor.execute("DELETE FROM users WHERE uid = %s", (request.form["userID"], ))
      mydb.commit()

      # build users list
      cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s) and uid LIKE (%s) and user_type LIKE (%s)", (first_name, last_name, uid, user_type))
      lookup_results = cursor.fetchall()
      session["sysadmin_Lookup_Results"] = []
      for student in lookup_results:
        session["sysadmin_Lookup_Results"].append(student)

    else:
      user_id = request.form["userID"]
      fn = request.form["first_name"]
      mi = request.form["middle_initial"]
      ln = request.form["last_name"]
      ad = request.form["address"]
      ut = request.form["user_type"]
      bd = request.form["birthday"]
      phone_no = request.form["phone_no"]
      ssn = request.form["ssn"]
      email = request.form["email"]
      cursor.execute('''
      UPDATE users 
      SET fname = (%s), 
          minit = (%s), 
          lname = (%s), 
          address = (%s), 
          birthday = (%s), 
          phone_no = (%s), 
          ssn = (%s), 
          email = (%s),  
          user_type = (%s) 
          WHERE uid = (%s)''', 
                     (fn, mi, ln, ad, bd, phone_no, ssn, email, ut, user_id))
      mydb.commit()

      # build users list
      cursor.execute("SELECT * FROM users WHERE fname LIKE (%s) and lname LIKE (%s) and uid LIKE (%s) and user_type LIKE (%s)", (first_name, last_name, uid, user_type))
      lookup_results = cursor.fetchall()
      session["sysadmin_Lookup_Results"] = []
      for student in lookup_results:
        session["sysadmin_Lookup_Results"].append(student)

  return render_template("sysadmin_regestration.html")

# Transcript page
@app.route('/Transcript<student_uid>', methods = ['GET', 'POST'])
def Transcript(student_uid):
  cursor = mydb.cursor(dictionary=True)
  # doesn't allow access if not logged in
  if "user_type" not in session:
    return redirect(url_for("logout"))
  
  # Faculty can only see the grades of there students
  if request.method == 'POST': #advisors
    if "sec_id" in request.form:
      section_id = request.form["sec_id"]
      new_grade = request.form["new_grade"]
      cursor.execute("UPDATE enrollment SET grade = %s WHERE student_uid = %s AND section_id = %s", (new_grade, student_uid, section_id, ))
      mydb.commit()
      flash("grade changed successfully")
  elif session['user_type'] == 'faculty': #teachers
    cursor.execute('''
    SELECT enrollment.student_uid
    FROM sections
        JOIN enrollment ON sections.section_id = enrollment.section_id
    WHERE sections.professor_uid = %s''',
                  (session['id'], ))
    all_students = cursor.fetchall()
    if {'student_uid': student_uid} not in all_students:
      return redirect(url_for("logout"))
  elif session['user_type'] == 'student_phd' or session['user_type'] == 'student_ms':
    if student_uid != session['id']:
      return redirect(url_for("logout"))
    
  cursor.execute('SELECT fname, minit, lname FROM users WHERE users.uid = %s', 
                (student_uid, ))
  session['student_name'] = cursor.fetchone()
  
  session['classes_taken'] = []
  cursor.execute('''
  SELECT * 
  FROM enrollment 
    JOIN classes ON classes.cid = enrollment.cid 
    JOIN sections ON enrollment.section_id = sections.section_id 
    JOIN users ON users.uid = sections.professor_uid 
  WHERE enrollment.student_uid = %s''',
                (student_uid, ))
  session['classes_taken'] = cursor.fetchall()

  cursor.execute('''
  SELECT grade 
  FROM enrollment JOIN classes ON classes.cid = enrollment.cid 
    JOIN sections ON enrollment.section_id = sections.section_id 
    JOIN users ON users.uid = sections.professor_uid 
  WHERE enrollment.student_uid = %s''',
                (student_uid, ))
  grades = cursor.fetchall()
  grades = [list(dct.values())[0] for dct in grades]
  possible_grades = ['IP', 'F', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A']

  # Calculate GPA
  x = requirement(student_uid)
  session['GPA'] = x["gpa"]
  session['Total_credit'] = x["tc"]

  return render_template('Transcript.html', student_uid = student_uid, grades = possible_grades)

# Class Page page
# TODO: calls to database student will be a univsersity ID
@app.route('/Class_Page<class_ID>', methods = ['GET', 'POST'])
def Class_Page(class_ID):
  # class_ID is a section id
  cursor = mydb.cursor(dictionary=True)
  if "user_type" not in session:
    return redirect(url_for("logout"))
  
  session['different_periods'] = ['3-5:30pm', '4-6:30pm', '6-8:30pm']
  session['different_periods_2'] = ['blank', '3-5:30pm', '4-6:30pm', '6-8:30pm']
  
  cursor.execute('''
  SELECT * 
  FROM sections 
      JOIN classes ON sections.cid = classes.cid 
      LEFT JOIN enrollment ON enrollment.section_id = sections.section_id 
      JOIN users ON users.uid = sections.professor_uid 
  WHERE sections.section_id = %s''',
                (class_ID, ))
  session['course'] = cursor.fetchone()
  try:
    cursor.fetchall() # so cursor doesn't have a fit when I try to use it again
  except:
    pass

  cursor.execute('''
  SELECT * 
  FROM enrollment 
    JOIN users ON users.uid = enrollment.student_uid 
  WHERE enrollment.section_id = (%s)''',
                 (class_ID, ))
  session['students'] = cursor.fetchall()

  session['possible_grades'] = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F', 'IP']

  if request.method == 'POST':
    student_uid = list(request.form.keys())[0]
    new_grade = request.form[student_uid]
    if session['user_type'] == 'faculty' and session['course']['professor_uid'] != session['id']:
      pass # teachers can't change grades for other classes
    elif new_grade == 'IP':
      cursor.execute('UPDATE enrollment SET grade = %s, finalized = 0 WHERE student_uid = %s AND section_id = %s',
                   (new_grade, student_uid, class_ID))
      mydb.commit()
    else:
      cursor.execute('UPDATE enrollment SET grade = %s, finalized = 1 WHERE student_uid = %s AND section_id = %s',
                   (new_grade, student_uid, class_ID))
      mydb.commit()

    cursor.execute('''
    SELECT * 
    FROM enrollment 
      JOIN users ON users.uid = enrollment.student_uid 
    WHERE enrollment.section_id = (%s)''',
                 (class_ID, ))
    session['students'] = cursor.fetchall()
  
  return render_template('Class_Page.html', class_ID = class_ID)

#-----------------------------------------------------------------------------------------------------------------
# APPS FUNCTIONS:
@app.route('/view_app')
def viewapp():
  if not 'id' in session:
     return stop_that()
  cursor = mydb.cursor(dictionary=True)
  cursor.execute("SELECT * FROM applications WHERE uid = %s;", (session['id'],))
  data = cursor.fetchall()
  return render_template('view_app.html', content = data)
  

@app.route('/edit_app/<semester>/<year>')
def editapp(semester, year):
  if not 'id' in session:
     return stop_that()
  cursor = mydb.cursor(dictionary=True)
  cursor.execute("SELECT * FROM applications WHERE uid = %s AND semester = %s AND s_year = %s", (session['id'], semester, year))
  app = cursor.fetchone()
  if app == None:
     stop_that()
  return render_template('edit_app.html', app = app)

@app.route('/update_app/<semester>/<year>', methods=['POST'])
def updateapp(semester, year):
  cursor = mydb.cursor(dictionary=True)
  prior_bac_deg_gpa = request.form["prior_bac_deg_gpa"]
  prior_bac_deg_major = request.form["prior_bac_deg_major"]
  prior_bac_deg_year = request.form["prior_bac_deg_year"]
  prior_bac_deg_university = request.form["prior_bac_deg_university"]
  prior_ms_deg_gpa = request.form["prior_ms_deg_gpa"]
  prior_ms_deg_major = request.form["prior_ms_deg_major"]
  prior_ms_deg_year = request.form["prior_ms_deg_year"]
  prior_ms_deg_university = request.form["prior_ms_deg_university"]
  gre_verbal = request.form["GRE_verbal"]
  gre_year = request.form["GRE_year"]
  gre_quantitative = request.form["GRE_quantitative"]
  gre_analytical_writing = request.form["GRE_analytical_writing"]
  toefl_score = request.form["TOEFL_score"]
  toefl_date = request.form["TOEFL_date"]
  interest = request.form["interest"]
  experience = request.form["experience"]
  cursor.execute('''UPDATE applications SET prior_bac_deg_gpa = %s, prior_bac_deg_major = %s, prior_bac_deg_year = %s, prior_bac_deg_university = %s, 
                  gre_verbal = %s, gre_year = %s, gre_quatitative = %s, gre_analytical_writing = %s, toefl_score = %s, toefl_date = %s, 
                  interest = %s, experience = %s, prior_ms_deg_gpa = %s, prior_ms_deg_major = %s, prior_ms_deg_year = %s, prior_ms_deg_university = %s WHERE uid = %s AND semester = %s AND s_year = %s''', 
                  (prior_bac_deg_gpa, prior_bac_deg_major, prior_bac_deg_year, prior_bac_deg_university, gre_verbal, gre_year, gre_quantitative, gre_analytical_writing, 
                   toefl_score, toefl_date, interest, experience, prior_ms_deg_gpa, prior_ms_deg_major, prior_ms_deg_year, prior_ms_deg_university, session['id'], semester, year))
  mydb.commit()
  flash("Application successfully updated")
  return redirect('/')

@app.route('/create_app', methods=['GET','POST'])
def createapp():
  if not 'id' in session:
     return stop_that()
  if request.method == 'POST':
    semester = request.form['semester']
    year = request.form['year']
    degree_type = request.form['degree_type']
    cursor = mydb.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM applications WHERE uid = %s AND semester = %s AND s_year = %s", (session['id'], semester, year))
    duplicate_app = not cursor.fetchone() == None
    if(duplicate_app):
      flash("You can't apply twice for the same term")
      return render_template('create_app.html')
    
    cursor.execute("INSERT INTO applications VALUES (%s, %s, %s, %s, %s, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')", 
                   ('incomplete', session['id'], semester, year, degree_type))
    mydb.commit()
    url = "/edit_app/" + semester + "/" + year
    return redirect(url)
  return render_template('create_app.html')

@app.route('/submit_app/<semester>/<year>', methods=['POST'])
def submitapp(semester, year):
  if(check_complete(session['id'], semester, year)):
    cursor = mydb.cursor()
    cursor.execute("UPDATE applications SET status = %s WHERE uid = %s AND semester = %s AND s_year = %s", ('complete', session['id'], semester, year))
    mydb.commit()
  else:
     flash("You are missing requirements!")
  return redirect('/view_app')

@app.route('/add_rec', methods=['GET', 'POST'])
def addrec():
   if not 'id' in session:
      return stop_that()
   if request.method == "POST":
      cursor = mydb.cursor(dictionary=True, buffered=True)

      cursor.execute("SELECT * FROM recommendations WHERE uid = %s", (session['id'],))
      duplicate = not cursor.fetchone() == None
      if duplicate:
         cursor.execute("DELETE FROM recommendations WHERE uid = %s", (session['id'],))
         mydb.commit()

      data = [[request.form['name0'], request.form['email0'], request.form['affiliation0'], request.form['content0']], 
              [request.form['name1'], request.form['email1'], request.form['affiliation1'], request.form['content1']], 
              [request.form['name2'], request.form['email2'], request.form['affiliation2'], request.form['content2']]]
      for i in range(3):
         cursor.execute("INSERT INTO recommendations VALUES (%s, %s, %s, %s, %s, %s)", (session['id'], i+1, data[i][3], data[i][0], data[i][2], data[i][1]))
         mydb.commit()
      return redirect('/')
   return render_template('add_rec.html')

def check_complete(id, semester, year):
   cursor=mydb.cursor(dictionary=True, buffered=True)
   cursor.execute("SELECT * FROM applications INNER JOIN recommendations ON applications.uid = recommendations.uid WHERE recommendations.uid=%s AND semester=%s AND s_year = %s", (id, semester, year))
   result = cursor.fetchone()
   if result != None and result['contents'] != None and result['recieved_transcript'] == True:
      return True
   return False

@app.route('/review_app')
def reviewapp():
   if not 'id' in session:
      return stop_that()
   cursor=mydb.cursor(dictionary=True)
   cursor.execute("SELECT * FROM applications")
   apps = cursor.fetchall()
   cursor.execute("SELECT * FROM recommendations")
   recs = cursor.fetchall()
   cursor.execute("SELECT * FROM applications WHERE uid NOT IN (SELECT student_id FROM reviews WHERE review_id = %s)", (session['id'],))
   not_my = cursor.fetchall()
   return render_template('review_app.html', apps = apps, recs = recs, not_my = not_my)

@app.route('/recieved/<uid>/<semester>/<year>', methods=["POST"])
def recieved(uid, semester, year):
   cursor=mydb.cursor()
   cursor.execute("UPDATE applications SET recieved_transcript = True WHERE uid = %s AND semester = %s AND s_year = %s", (uid, semester, year))
   mydb.commit()
   return redirect('/review_app')

@app.route('/review/<uid>/<semester>/<year>', methods=["GET", "POST"])
def review(uid, semester, year):
  if not 'id' in session:
    return stop_that()
  cursor=mydb.cursor(dictionary=True)
  if request.method=="POST":
    cursor.execute("SELECT * FROM reviews WHERE review_id = %s AND student_id = %s AND p_semester = %s AND p_year = %s", (session['id'], uid, semester, year))
    duplicate = not cursor.fetchone() == None
    if duplicate:
      cursor.execute("DELETE FROM reviews WHERE review_id = %s AND student_id = %s AND p_semester = %s AND p_year = %s", (session['id'], uid, semester, year))
      mydb.commit()
    rating = request.form.get("rating")
    deficiency = request.form.get("deficiency")
    why = request.form.get("reason_reject")
    comment = request.form.get("comment")
    cursor.execute("INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '', '')", (session['id'], uid, semester, year, rating, deficiency, why, comment))
    cursor.execute("UPDATE applications SET status = 'under review' WHERE uid = %s AND semester = %s AND s_year = %s", (uid, semester, year))
    mydb.commit()
    flash("Submitted review")
    return redirect('/review_app')
  cursor.execute("SELECT * FROM applications WHERE uid = %s AND semester = %s AND s_year = %s", (uid, semester, year))
  app = cursor.fetchone()
  cursor.execute("SELECT * FROM recommendations WHERE uid = %s", (uid,))
  rec = cursor.fetchall()
  return render_template('write_review.html', app = app, rec = rec)

@app.route('/final_review/<uid>/<semester>/<year>', methods=["GET", "POST"])
def finalreview(uid, semester, year):
  if not 'id' in session:
    return stop_that()
  cursor=mydb.cursor(dictionary=True)
  if request.method=="POST":
    decision = request.form["decision"]
    cursor.execute("UPDATE applications SET status = %s WHERE uid = %s AND semester = %s AND s_year = %s", (decision, uid, semester, year))
    mydb.commit()
    flash("Submitted")
    return redirect('/review_app')
  cursor.execute("SELECT * FROM applications WHERE uid = %s AND semester = %s AND s_year = %s", (uid, semester, year))
  app = cursor.fetchone()
  cursor.execute("SELECT * FROM recommendations WHERE uid = %s", (uid,))
  rec = cursor.fetchall()
  cursor.execute("SELECT * FROM reviews WHERE student_id = %s AND p_semester = %s AND p_year = %s", (uid, semester, year))
  rev = cursor.fetchall()
  return render_template('write_final_review.html', app = app, rec = rec, rev = rev)
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if "user_type" not in session:
       return redirect('/')
    if session['user_type'] != "admin":
       return redirect('/')
    cursor = mydb.cursor(dictionary=True)
    with open('create.sql', 'r') as f:
        sql_script = f.read()
    sql_commands = sql_script.split(';')
    for command in sql_commands:
        cursor.execute(command)
        while True:
            try:
                cursor.nextset()
            except mysql.connector.errors.InterfaceError:
                break
    mydb.commit()
    session.clear()
    return redirect('/')


@app.route('/enroll/<deg>', methods=['POST'])
def enroll(deg):
  cursor=mydb.cursor(dictionary=True)
  if deg=='MS':
    new = 'student_ms'
  else:
     new = 'student_phd'
  cursor.execute("UPDATE users SET user_type=%s WHERE uid=%s", (new, session['id']))
  mydb.commit()
  flash("Congratulations!")
  return redirect('/')

# Error handling
@app.errorhandler(400)
def bad_request(e):
   flash("Bad!")
   return redirect('/')

@app.errorhandler(404)
def not_found(e):
   flash("These are not the droids you are looking for!")
   return redirect('/')

@app.errorhandler(405)
def not_allowed(e):
   flash("You're doing it wrong!")
   return redirect('/')

def stop_that():
   flash("Stop that!")
   return redirect('/')

app.run(host='0.0.0.0', port=9080)

