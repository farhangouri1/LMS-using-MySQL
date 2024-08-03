from tkinter import *
from tkinter import font
from tkinter.messagebox import showinfo
import mysql.connector as mysql
from PIL import ImageTk, Image
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd

# FOR CHANGING ADMIN USERNAME AND PASSWORD
admin = 'Admin'
password = '12345'



# DEFINING FUNTIONS
def quit():
    faru.destroy()



def newBook():
    def topUp_destroy():
        top_up1.destroy()
    def newBookSql():
        try:
            userName_entry.delete(0,END)
            password_entry.delete(0,END)

            value = (bookNameEntry.get(),bookClassEntry.get(),bookEditionEntry.get())
            worker.execute("create table if not exists books (bookName varchar(30),class varchar(5),edition varchar(5))")
            worker.execute('insert into books values(%s,%s,%s)',value)
            db.commit()

            bookNameEntry.delete(0,END)
            bookClassEntry.delete(0,END)
            bookEditionEntry.delete(0,END)

            show_details()
        except Exception as f:
            showinfo('ERROR!!!','Something went wrong! Please try again later')
            top_up1.destroy()
            print(f)

    uservalue = userName_entry.get()
    passvalue = password_entry.get()
    if uservalue == admin and passvalue == password:
        top_up1 = Toplevel()
        top_up1.geometry('400x500+880+120')
        top_up1.maxsize(400, 500)
        top_up1.configure(bg='cyan')

        frame1 = Frame(top_up1)
        frame1.pack()
        bookNameLabel = Label(top_up1,text=' BookName ', bg='cyan', font='cosmic 15 bold')
        bookClassLabel = Label(top_up1,text=' Class ', bg='cyan', font='cosmic 15 bold')
        bookEditionLabel = Label(top_up1,text='  Edition ', bg='cyan', font='cosmic 15 bold')
        bookNameLabel.place(x=50, y=50)
        bookClassLabel.place(x=50, y=100)
        bookEditionLabel.place(x=48, y=150)
        
        bookNameEntry = Entry(top_up1)
        bookClassEntry = Entry(top_up1)
        bookEditionEntry = Entry(top_up1)
        bookNameEntry.place(y=55, x=180)
        bookClassEntry.place(y=100, x=180)
        bookEditionEntry.place(y=145, x=180)
        
        b1 = Button(top_up1,text='    Done    ', relief=GROOVE, font='cosmic 12 bold', bg='cyan',command=newBookSql)
        b1.place(x=160, y= 200)
        b2 = Button(top_up1,text='    EXIT    ', relief=GROOVE, font='cosmic 12 bold', bg='cyan',command=topUp_destroy)
        b2.place(x=160, y= 250)

    else:
        showinfo('invalid', 'username or password invalid')


def borrow_book():
    def end():
        top_up2.destroy()
    def borrowSql():
        book_name = e2Var.get()
        book_class = e4Var.get()
        book_edition = e3Var.get()
        value = (e1Var.get(),e2Var.get(),e3Var.get(),e4Var.get())
        temp = (book_name,book_class,book_edition)
        try:
            sql1='''create table IF NOT EXISTS borrower (borrower_name varchar(25),
            book_name varchar(30), edition varchar(10), class varchar(7))'''
            sql2 = """DELETE from books where bookName = %s AND edition = %s"""

            worker.execute('select * from books')
            data = worker.fetchall()

            if temp in data:
                worker.execute(sql1)
                worker.execute(sql2,(book_name,book_edition))
                db.commit()

                worker.execute('insert into borrower values(%s,%s,%s,%s)',value)
                db.commit()
                top_up2.destroy()
                show_details()
                showinfo('Congratulation','Hope you will like this book 😊\nplease return on time.')
            else:
                showinfo('Sorry ☹','Sorry book is not available')
                top_up2.destroy()
            


        except Exception as f:
            showinfo('ERROR 😱','You got some error')
            top_up2.destroy()
            print(f)


    top_up2 = Toplevel()
    top_up2.geometry('400x500+0+0')
    top_up2.configure(bg='maroon')
    top_up2.maxsize(400, 500)
    frame5 = Frame(top_up2)
    frame5.pack()
    l1 = Label(top_up2, text='Your Name', bg="maroon", fg='white',font='cosmic 12 bold')  
    l2 = Label(top_up2, text='Book Name', bg="maroon", fg='white',font='cosmic 12 bold')    
    l3 = Label(top_up2, text='Edition', bg="maroon", fg='white',font='cosmic 12 bold')    
    l4 = Label(top_up2, text='Class', bg="maroon", fg='white',font='cosmic 12 bold')    
    l1.place(x=20, y=50)
    l2.place(x=20, y=100)
    l3.place(x=20, y=150)
    l4.place(x=20, y=200)

    global e1Var,e2Var,e3Var,e4Var
    e1Var = StringVar()
    e2Var = StringVar()
    e3Var = StringVar()
    e4Var = StringVar()

    e1 = Entry(top_up2,textvariable=e1Var)
    e2 = Entry(top_up2,textvariable=e2Var)
    e3 = Entry(top_up2,textvariable=e3Var)
    e4 = Entry(top_up2,textvariable=e4Var)
    e1.place(x=170, y=50)
    e2.place(x=170, y=100)
    e3.place(x=170, y=150)
    e4.place(x=170, y=200)

    b1 = Button(top_up2, text=' Borrow ', bg='maroon', relief=RAISED, font='cosmic 13 bold',command=borrowSql)
    b2 = Button(top_up2, text='    Exit    ', bg='maroon', relief=RAISED, font='cosmic 13 bold', command=end)
    b1.place(x=50, y=250)
    b2.place(x=200, y=250)


def return_book():
    def end():
        top_up3.destroy()
    def returnSql():
        try:
            b_name = entry1.get()
            name = entry2.get()
            b_edition = entry3.get()
            values = (b_name,name,b_edition)
            sql = '''DELETE from borrower where borrower_name = %s
            AND book_name = %s
            AND edition = %s'''
            worker.execute(sql,values)
            db.commit()

            value = (entry2.get(),entry4.get(),entry3.get())
            print(value)
            worker.execute('insert into books values(%s,%s,%s)',value)
            db.commit()
            top_up3.destroy()

        except Exception as f:
            showinfo('ERROR 😱','Something went wrong')
            top_up3.destroy()
            print(f)

    top_up3 = Toplevel()
    top_up3.geometry('300x400')
    top_up3.configure(bg='lightblue1')

    l1 = Label(top_up3, text='Your Name', font='cosmic 13 bold', bg='lightblue1')
    label2 = Label(top_up3, text='Book Name', font='cosmic 13 bold', bg='lightblue1')
    label3 = Label(top_up3, text='Book Edition', font='cosmic 13 bold', bg='lightblue1')
    label4 = Label(top_up3, text='Class', font='cosmic 13 bold', bg='lightblue1')
    l1.place(x=20, y=50)
    label2.place(x=20, y=100)
    label3.place(x=20, y=150)
    label4.place(x=20, y=200)

    entry1 = Entry(top_up3)
    entry2 = Entry(top_up3)
    entry3 = Entry(top_up3)
    entry4 = Entry(top_up3)
    entry1.place(x=130, y=50)
    entry2.place(x=130, y=100)
    entry3.place(x=130, y=150)
    entry4.place(x=130, y=200)

    b1 = Button(top_up3, text='   Done   ', bg='lightblue1', relief=RAISED,command=returnSql)
    b2 = Button(top_up3, text='   Exit   ', bg='lightblue1', relief=RAISED, command=end)
    b1.place(x=40,y=250)
    b2.place(x=190,y=250)


def dataOnClick(ev):
    try:
        selectedRow = bookDetails.focus()
        rowData = bookDetails.item(selectedRow)
        data = rowData['values']

        e2Var.set(data[0])
        e4Var.set(data[1])
        e3Var.set(data[2])
    except Exception as f:
        print(f)

def show_details():
    try:
        db = mysql.connect(host="localhost", user="root", password="", database="library")
        worker = db.cursor()
        worker.execute('select * from books')
        fetchData = worker.fetchall()
        if len(fetchData) != 0:
            for item in bookDetails.get_children():
                bookDetails.delete(item)
            for f in fetchData:
                bookDetails.insert('', END,values = f)
                db.commit()



    except Exception as e:
        print(e)
        pass


def showCondition_details():
    try:
        db = mysql.connect(host="localhost", user="root", password="", database="library")
        worker = db.cursor()

        worker.execute("select * from books where "+str(searchBy.get())+" LIKE '%"+str(searchText.get())+"%'")
        fetchData = worker.fetchall()
        if len(fetchData) != 0:
            for item in bookDetails.get_children():
                bookDetails.delete(item)
            for f in fetchData:
                bookDetails.insert('', END,values = f)
                db.commit()



    except Exception as e:
        pass


def showGraph():
        db = mysql.connect(host="localhost", user="root", password="", database="library")
        worker = db.cursor()
        list1 = []
        for f in range(1,13):
            sql = '''select class from books where class = %s'''
            worker.execute('select count(class) from books where class ='+str(f))
            data = worker.fetchall()
            list1.append(data)
            
        db.commit()
        list2 = []
        for var1 in list1:
            for var2 in var1:
                for var3 in var2:
                    list2.append(var3)

        labels = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th',]
        #plt.pie(list2,labels=labels)
        plt.bar(labels, list2,width=0.5)
        plt.ylabel('NO. Of Books')
        plt.xlabel('Classes')
        plt.title('Class wise no. of books')
        plt.show()

    
faru = Tk()
width= faru.winfo_screenwidth()
height= faru.winfo_screenheight()
faru.geometry("%dx%d" % (width, height))
faru.configure(bg='cyan')
faru.title('LIBRARY MANAGEMENT')

global searchBy,searchText
searchBy = StringVar()
searchText = StringVar()

# MAKING FRAMES
label1 = Label(faru,text="DMS LIBRARY",font=('times new roman',35,'bold'),bg='red',fg='black')
label1.pack(side=TOP,anchor='n',fill=X)

frame1 = Frame(faru,bg='skyblue',borderwidth=5,relief=FLAT,height=550)
frame1.place(x=15,y=75,width=350,height=550)

frame2 = Frame(faru,bg='skyblue',borderwidth=5,relief=FLAT,height=550)
frame2.place(x=380,y=75,width=565,height=550)

frame3 = Frame(faru,bg='skyblue',borderwidth=5,relief=FLAT,height=550)
frame3.place(x=960,y=75,width=300,height=550)

# BUTTONS FRAME
show_button = Button(frame1,bg='azure',fg='black',text='  SHOW BOOK  ',font=('',15,'bold'),relief=RAISED,width=15)
borrow_button = Button(frame1,bg='azure',fg='black',text='  ISSUE BOOK ',font=('',15,'bold'),relief=RAISED,width=15,command=borrow_book)
return_button = Button(frame1,bg='azure',fg='black',text='  RETURN BOOK ',font=('',15,'bold'),relief=RAISED,width=15,command=return_book)
graph_button = Button(frame1,bg='azure',fg='black',text='  SHOW GRAPH ',font=('',15,'bold'),relief=RAISED,width=15,command=showGraph)
exit_button = Button(frame1,bg='azure',fg='black',text='  EXIT  ',font=('',15),relief=RAISED,width=10,command=quit)
show_button.place(x=65,y=15)
borrow_button.place(x=65,y=95)
return_button.place(x=65,y=175)
graph_button.place(x=65,y=255)
exit_button.place(x=92,y=335)

# ADMIN FRAME
newBook_label = Label(frame3,text='For Adding Book',font=('',18,'bold'),bg='skyblue')
newBook_label.pack(side=TOP,fill=X,pady=10)

userName_label = Label(frame3,text='Username: ',font=('',13),bg="skyblue")
password_label = Label(frame3,text='Password: ',font=('',13),bg="skyblue")
userName_label.place(x=10,y=50)
password_label.place(x=10,y=85)

userName_entry = Entry(frame3)
password_entry = Entry(frame3,show='*')
userName_entry.place(x=120,y=51)
password_entry.place(x=120,y=86)

button1 = Button(frame3,text='DONE',font=('',12,'bold'),command=newBook)
button1.place(x=120,y=140)

try:
    bg = ImageTk.PhotoImage(Image.open("logo.jpg"))
    # Create Canvas
    canvas1 = Canvas( frame3, width = 230,
                     height = 225)
    
    canvas1.pack(side=LEFT,anchor='sw', expand = True,padx=30,pady=30)

    # Display image
    canvas1.create_image( 115,5, image = bg, 
                         anchor = "n")
except:
    pass
        


# DISPLAY FRAME
labelSearch=Label(frame2, text="Search By:", bg="skyblue",fg="black", font=("times new roman", 15, "bold"))
labelSearch.grid(row=0, column=0, pady=10, padx=10,sticky="w")

comboSearch=ttk.Combobox (frame2,textvariable=searchBy ,font=("times new roman",13,"bold"), state='readonly',width=10)
comboSearch ['values']=("bookName", "Class", "Edition")
comboSearch.grid(row=0, column=1, padx=0, pady=10)

txt_Search=Entry (frame2,textvariable=searchText ,font=("times new roman", 14, "bold"), bd=3,relief=GROOVE,width=10)
txt_Search.grid(row=0,column=2, pady=10, padx=10,sticky="w")

searchButton=Button(frame2, text="Search",width=10,command=showCondition_details)
searchButton.grid (row=0, column=3, padx=10, pady=10)
showAllButton = Button(frame2, text="Show All",width=10,command=show_details)
showAllButton.grid (row=0, column=4, padx=10, pady=10)

frame4=Frame (frame2, bd=4, relief=RIDGE, bg="white")
frame4.place(x=10,y=50,width=535,height=500)
yAxis =Scrollbar (frame4, orient=VERTICAL)
bookDetails = ttk.Treeview(frame4,columns=('bookName','class','edition'),yscrollcommand=yAxis.set)
yAxis.pack(side=RIGHT,fill=Y)
yAxis.config(command=bookDetails.yview)
bookDetails.heading('bookName',text='Book Name')
bookDetails.heading('class',text='Class')
bookDetails.heading('edition',text='Edition')
bookDetails['show'] = 'headings'

bookDetails.column('bookName',width=279)
bookDetails.column('class',width=112)
bookDetails.column('edition',width=112)
bookDetails.bind('<ButtonRelease-1>',dataOnClick)
bookDetails.pack(fill=BOTH,expand=1)
show_details()


# CHECKING SERVER IS CONNECTED OR NOT
try:
    db = mysql.connect(host="localhost", user="root", password="", database="library")
    worker = db.cursor()
except:
    showinfo('ERROR 😱','Please start your mysql local server 🙄')
    exit()
    

faru.mainloop()