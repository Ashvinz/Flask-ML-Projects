import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('Employee_management.db')

cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS EMPLOYEE_MANAGEMENT (EMPLOYEE_NAME TEXT, CONTACT_NO TEXT, DESTINATION TEXT, HIRE_DATE TEXT, SALARY TEXT)"
)

# Creating the functions
def reset_fields():
   global name_strvar, contact_strvar, destination_strvar, salary_strvar

   for i in ['name_strvar', 'contact_strvar', 'destination_strvar', 'salary_strvar']:
       exec(f"{i}.set('')")
   hiredate.set_date(datetime.datetime.now().date())

def reset_form():
   global tree
   tree.delete(*tree.get_children())

   reset_fields()

def display_records():
   tree.delete(*tree.get_children())

   curr = connector.execute('SELECT * FROM EMPLOYEE_MANAGEMENT')
   data = curr.fetchall()

   for records in data:
       tree.insert('', END, values=records)

def add_record():
   global name_strvar, contact_strvar, destination_strvar, hiredate_strvar, salary_strvar

   name = name_strvar.get()
   contact = contact_strvar.get()
   destination = designation_strvar.get()
   hiredate = hiredate_strvar.get()
   salary = slary_strvar.get()

   if not name or not contact or not destination or not hiredate or not slary:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO EMPLOYEE_MANAGEMENT (NAME, CONTACT_NO, DESTINATION, HIRE_DATE, SALARY) VALUES (?,?,?,?,?)', (name, contact, designation, hiredate, salary)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]

       tree.delete(current_item)

       connector.execute('DELETE FROM EMPLOYEE_MANAGEMENT WHERE EMPLOYEE_ID=%d' % selection[0])
       connector.commit()

       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

       display_records()


def view_record():
   global name_StrVar, contact_StrVar, destination_StrVar, hiredate_StrVar, salary_StrVar

   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]

   date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

   name_StrVar.set(selection[1]); contact_StrVar.set(selection[2])
   destination_StrVar.set(selection[3]); hiredate_StrVar.set(selection[4])
   salary_StrVar.set(selection[5])


# Initializing the GUI window
main = Tk()
main.title('DataFlair Employee_Management System')
main.geometry('1000x600')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frame

# Creating the StringVar or IntVar variables
Name_StrVar = StringVar()
Contact_StrVar = StringVar()
Destination_StrVar = StringVar()
Salary_StrVar = StringVar()

# Placing the components in the main window
Label(main, text="EMPLOYEE_MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.05)
Label(left_frame, text="Contact_No", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.15)
Label(left_frame, text="Destination", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.25)
Label(left_frame, text="Hire_Date", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.35)
Label(left_frame, text="Salary", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.45)

Entry(left_frame, width=19, textvariable=Name_StrVar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=Contact_StrVar, font=entryfont).place(x=20, rely=0.11)
Entry(left_frame, width=19, textvariable=Destination_StrVar, font=entryfont).place(x=20, rely=0.21)
Entry(left_frame, width=19, textvariable=Salary_StrVar, font=entryfont).place(x=20, rely=0.31)

hire = DateEntry(left_frame, font=("Arial", 12), width=15)
hire.place(x=20, rely=0.62)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)

# Placing components in the right frame
Label(right_frame, text='Employee Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Employee ID', "Name", "Contact_No", "Designation", "Hire_Date", "Salary"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Employee ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Contact_No', text='Contact_No', anchor=CENTER)
tree.heading('Designation', text='Destination', anchor=CENTER)
tree.heading('Hire_Date', text='Hire_Date', anchor=CENTER)
tree.heading('Salary', text='Salary', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=120, stretch=NO)




tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()





