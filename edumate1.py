from tkinter import * 
from tkinter import messagebox 
import re, pymysql 

def adjustWindow(window):
    w = 600
    h = 600
    ws = screen.winfo_screenwidth()
    hs = screen.winfo_screenheight()
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2) 
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))  
    window.resizable(False, False)     
    window.configure(background='white')
        
def enter_new_record(entryField,semester,stu_roll): 
    found = 0 
    for student in entryField: 
        for field in student: 
            if(field.get() == ""):
                found = 1 
                break 
    if found == 0: 
          if semester.get() == '--0--':
              messagebox.showerror("Error", "Please select semester", parent=screen4)  
          else: 
            
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") 
            cursor = connection.cursor()     
            for fields in entryField:  
                cursor.execute("""INSERT INTO student_records (subject_name, marks_scored, out_off, credit_point, semester,student_roll) VALUES(%s,%s,%s,%s,%s,%s)""",(fields[0].get(),str(fields[1].get()),str(fields[2].get()),str(fields[3].get()),str(semester.get()),str(stu_roll.get())))
            connection.commit() 
            connection.close()  
            messagebox.showinfo("Congratulation", "Entry Succesfull",parent=screen4) 
            screen4.destroy()       
    else:
        messagebox.showerror("Error", "Please fill all the details", parent=screen4) 
def student_new_record():
    global screen4
    stu_roll=StringVar()
    semester = StringVar()
    entryField = list() 
    screen4 = Toplevel(screen) 
    screen4.title("New Record") 
    adjustWindow(screen4)
    screen4.configure(bg="#174873")
    Label(screen4, text="Enter New Record", width='40', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4) 
    Label(screen4, text="", bg='white').grid(row=1,column=0)

    Label(screen4, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=0, pady=(5,10)) 
    Label(screen4, text="Marks", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=1, pady=(5,10)) 
    Label(screen4, text="Out of", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=2, pady=(5,10)) 
    Label(screen4, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=3, pady=(5,10)) 
    rowNo = 3
    for i in range(6):  
        temp = list() 
        for j in range(4): 
            e = Entry(screen4, width=14) 
            e.grid(row=rowNo,column=j, padx=(3,0), pady=(0,25)) 
            temp.append(e)
        entryField.append(temp) 
        rowNo += 2 
    Label(screen4, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=rowNo,column=0, pady=(15,0)) 
    list1 = ['1','2','3','4','5','6','7','8'] 
    droplist = OptionMenu(screen4, semester, *list1) 
    semester.set('--0--') 
    droplist.config(width=5) 
    droplist.grid(row=rowNo, column=1, pady=(15,0))
    Label(screen4, text="Student rollno", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=rowNo,column=2, pady=(15,0)) 
    Entry(screen4, textvar=stu_roll).grid(row=rowNo,column=3, pady=(15,0)) 
    Button(screen4, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='#e79700', fg='white', command=lambda: enter_new_record(entryField, semester,stu_roll)).grid(row=rowNo+6,columnspan=2,column=1, pady=(15,0))
 
def admin_verify():
    username = user_name.get() 
    password = pass_word.get()
    if (username == 'admin' and  password == 'secret'):
        messagebox.showinfo("Congratulation", "Login Succesfull")
        student_new_record()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")
         
def admin():
    global screen5,user_name,pass_word
    screen5=Toplevel(screen)
    user_name = StringVar() 
    pass_word = StringVar()    
    screen5.title("ADMIN-LOGIN")
    adjustWindow(screen5)  
    Label(screen5, text="edumate -ADMIN LOGIN", width="500", height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').pack() 
    Label(text="", bg='white').pack()  
    Label(screen5, text="", bg='#174873',width='72', height='30').place(x=45, y=120)
    Label(screen5, text="", bg='#174873').pack()
    Label(screen5, text="Please enter details below to login", bg='#174873', fg='white',width='72').pack() 
    Label(screen5, text="", bg='#174873').pack()  
    Label(screen5, text="Username * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack() 
    Entry(screen5, textvar=user_name).pack() 
    Label(screen5, text="", bg='#174873').pack() 
    Label(screen5, text="Password * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack() 
    Entry(screen5, textvar=pass_word, show="*").pack()
    Label(screen5, text="", bg='#174873').pack()
    Button(screen5, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white',command=admin_verify).pack()#, command=login_verify
    Label(screen5, text="", bg='#174873').pack()
    photo = PhotoImage(file="admin.png")
    label = Label(screen5, image=photo, text="",)
    label.place(x=204, y=350)
    label.image = photo 

def fetch_record(semester,roll):
    
    if semester == '--0--':
        messagebox.showerror("Error", "Please select proper semester", parent=screen4) 
    else: 
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") 
        cursor = connection.cursor() 
        select_query =  "SELECT subject_name, marks_scored, out_off, credit_point FROM student_records where semester = " + str(semester.get()) + " AND student_roll = " + str(roll.get()) + ";" # queries for retrieving values 
        cursor.execute(select_query)
        student_records = cursor.fetchall() 
        connection.commit()  
        connection.close() 
        if len(student_records) > 0: 
            for i in range(len(student_records)):
                for j in range(4): 
                    Label(screen3, text=student_records[i][j], font=("Open Sans", 11, 'bold'), fg='white', bg='#174873').grid(row=i+4,column=j, pady=(5,10)) 
            output = list() 
            for record in student_records: 
                temp = list() 
                per = (int(record[1])/int(record[2])) * 100 
                if per >= 80: 
                    temp.append(10) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 75 and per < 80: 
                    temp.append(9) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 70 and per < 75: 
                    temp.append(8) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 60 and per < 70: 
                    temp.append(7) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 50 and per < 60: 
                    temp.append(6) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 45 and per < 50: 
                    temp.append(5) 
                    temp.append(record[3]) 
                    output.append(temp) 
                elif per >= 40 and per < 45: 
                    temp.append(4) 
                    temp.append(record[3]) 
                    output.append(temp) 
                else: 
                    temp.append(0) 
                    temp.append(record[3]) 
                    output.append(temp) 
            credits_earned = total_credit_points = 0 
            for result in output: 
                credits_earned += result[0] * result[1] 
                total_credit_points += result[1] 
            cgpa = credits_earned/total_credit_points 
            percentage = 7.1 * cgpa + 11  
            Label(screen3, text="Your CGPI", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=0, pady=(15,10)) 
            Label(screen3, text=cgpa, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=1, pady=(15,10)) 
            Label(screen3, text="Percentage", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=2, pady=(15,10)) 
            Label(screen3, text=percentage, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=3, pady=(15,10)) 
        else: 
            messagebox.showerror("Error", "Entry not found", parent=screen3) 
            
def student_records(): 
    global screen3 
    semester = StringVar()
    roll=StringVar()
    screen3 = Toplevel(screen) 
    screen3.title("Student Records")
    adjustWindow(screen3)
    Label(screen3, text="Your Record", width='40', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4) 
    Label(screen3, text="", bg='#174873', width='81', height='30').place(x=17, y=100) 
    Label(screen3, text="", bg='white').grid(row=1,column=0)
    Label(screen3, text="Select rollno:", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=0, pady=(5,0))
    Entry(screen3,textvar=roll).grid(row=2,column=1, pady=(5,0))
    Label(screen3, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=2, pady=(5,0)) 
    list1 = ['1','2','3','4','5','6','7','8']
    droplist = OptionMenu(screen3, semester, *list1, command=lambda x: fetch_record(semester,roll)) 
    semester.set('--0--') 
    droplist.config(width=5) 
    droplist.grid(row=2, column=3, pady=(5,0))

    Label(screen3, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=0, pady=(15,10)) 
    Label(screen3, text="Your Marks", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=1, pady=(15,10)) 
    Label(screen3, text="Out of", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=2, pady=(15,10)) 
    Label(screen3, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=3, pady=(15,10)) 
          
def welcome_page(student_info): 
    global screen2 
    screen2 = Toplevel(screen) 
    screen2.title("Welcome") 
    adjustWindow(screen2) 
    screen2.configure(bg="#174873")
    Label(screen2, text="Welcome " + student_info[0][1], width='40', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').place(x=0, y=0) 
    
    photo = PhotoImage(file="book.png")
    label = Label(screen2, image=photo, text="")
    label.place(x=150, y=200)
    label.image = photo
    Message(screen2, text='" Some people dream of accomplishing great things. Others stay awake and make it happen. "\n\n - By Some Night Owl', width='400', font=("Helvetica", 12, 'bold', 'italic'), fg='white', bg='#174873', anchor = CENTER).place(x=100, y=100)
        
    Button(screen2, text='Check your result', width=20, font=("Open Sans", 13, 'bold'), bg='#e79700', fg='white', command=student_records).place(x=200, y=530) 

def register_user(): 
    if fullname.get() and email.get() and password.get() and repassword.get() and gender.get():  
        if password.get() != repassword.get():
            Label(screen1, text="Password does not match", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) 
            return 
        else: 
            if tnc.get(): 
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()):
                    gender_value = 'male'
                    if gender.get() == 2:
                        gender_value = 'female' 
                    connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") 
                    cursor = connection.cursor() 
                    insert_query = "INSERT INTO student_details (fullname, email, password, gender) VALUES('"+ fullname.get() + "', '"+ email.get() + "', '"+ password.get() + "', '"+ gender_value + "' );"  
                    cursor.execute(insert_query)
                    connection.commit() 
                    connection.close()
                    Label(screen1, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) 
                    Button(screen1, text='Proceed to Login ->', width=20, font=("Open Sans", 9, 'bold'), bg='brown', fg='white',command=screen1.destroy).place(x=170, y=565)  

                else: 
                    Label(screen1, text="Please enter valid email id", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) 
                    return 
            else: 
                Label(screen1, text="Please accept the agreement", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) 
                return 
    else: 
        Label(screen1, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) 
        return
    
def register(): 
    
    global screen1, fullname, email, password, repassword, gender, tnc 
    fullname = StringVar() 
    email = StringVar() 
    password = StringVar() 
    repassword = StringVar() 
    gender = IntVar() 
    tnc = IntVar() 
    screen1 = Toplevel(screen) 
    screen1.title("Registeration") 
    adjustWindow(screen1) 
    Label(screen1, text="Registration Form", width='40', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').place(x=0, y=0) 
    Label(screen1, text="", bg='#174873', width='72', height='30').place(x=45, y=120) 
    Label(screen1, text="Full Name:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=150, y=160) 
    Entry(screen1, textvar=fullname).place(x=300, y=160) 
    Label(screen1, text="Email ID:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=150, y=210) 
    Entry(screen1, textvar=email).place(x=300, y=210) 
    Label(screen1, text="Gender:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=150, y=260) 
    Radiobutton(screen1, text="Male", variable=gender, value=1, bg='#e79700').place(x=300, y=260) 
    Radiobutton(screen1, text="Female", variable=gender, value=2, bg='#e79700').place(x=370, y=260) 
    Label(screen1, text="Password:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=150, y=310) 
    Entry(screen1, textvar=password, show="*").place(x=300, y=305) 
    Label(screen1, text="Re-Password:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=150, y=360) 
    entry_4 = Entry(screen1, textvar=repassword, show="*") 
    entry_4.place(x=300, y=360) 
    Checkbutton(screen1, text="I accept all terms and conditions", variable=tnc, bg='#e79700', font=("Open Sans", 9, 'bold'), fg='brown').place(x=175, y=450) 
    Button(screen1, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='#e79700', fg='white', command=register_user).place(x=170, y=490) 
           
def login_verify():
    
    global studentID 
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate")  
    cursor = connection.cursor() 
    select_query =  "SELECT * FROM student_details where email = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';"  
    cursor.execute(select_query)  
    student_info = cursor.fetchall() 
    connection.commit() 
    connection.close()                      
    if student_info: 
        messagebox.showinfo("Congratulation", "Login Succesfull") 
        studentID = student_info[0][0] 
        welcome_page(student_info)  
    else: 
        messagebox.showerror("Error", "Invalid Username or Password")
          
def main_screen(): 
    global screen, username_verify, password_verify 
    screen = Tk()  
    username_verify = StringVar() 
    password_verify = StringVar() 
    screen.title("Edumate")  
    adjustWindow(screen)  
    Label(screen, text="Edumate - Student Marksheet Manager", width="500", height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').pack() 
    Label(text="", bg='white').pack()
    Label(screen, text="", bg='#174873',width='72', height='25').place(x=45, y=120) 
    Label(screen, text="Please enter details below to login", bg='#174873', fg='white',width='72').pack() 
    Label(screen, text="", bg='#174873').pack()  
    Label(screen, text="Username * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack() 
    Entry(screen, textvar=username_verify).pack() 
    Label(screen, text="", bg='#174873').pack() 
    Label(screen, text="Password * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack() 
    Entry(screen, textvar=password_verify, show="*").pack()
    Label(screen, text="", bg='#174873').pack()
    Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=login_verify).pack()
    Label(screen, text="", bg='#174873').pack()
    Button(screen, text="New User? Register Here", height="2", width="30", bg='#e79700', font=("Open Sans", 10, 'bold'), fg='white', command=register ).pack()
    Label(screen, text="", bg='#174873').pack()
    Button(screen, text="Admin? Login Here", height="2", width="30", bg='#e79700', font=("Open Sans", 10, 'bold'), fg='white',command=admin).pack()
    screen.mainloop()
    
 
main_screen()
"""      
--
-- Table structure for table `student_details`
--
CREATE TABLE `student_details` (
 `id` int(11) NOT NULL,
 `fullname` text NOT NULL,
 `email` text NOT NULL,
 `password` text NOT NULL,
 `gender` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `student_records`
--
CREATE TABLE `student_records` (
 `id` int(11) NOT NULL,
 `subject_name` text NOT NULL,
 `marks_scored` int(3) NOT NULL,
 `out_off` int(3) NOT NULL,
 `credit_point` int(1) NOT NULL,
 `semester` int(1) NOT NULL,
 `student_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for table `student_details`
--
ALTER TABLE `student_details`
 ADD PRIMARY KEY (`id`);
--
-- Indexes for table `student_records`
--
ALTER TABLE `student_records`
 ADD PRIMARY KEY (`id`);

 --
-- AUTO_INCREMENT for table `student_details`
--
ALTER TABLE `student_details`
 MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `student_records`
--
ALTER TABLE `student_records`
 MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;
"""
