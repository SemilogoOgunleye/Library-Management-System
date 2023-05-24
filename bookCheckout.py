import os
from tkinter import *
from csv import *
from tkinter import messagebox
import uuid
import re 
from database import load_log_file


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def only_email(val):
        if re.search(regex, val):
            return True
        else:
            msg = 'ENTER VALID EMAIL'
            messagebox.showerror(title=msg, message=msg)
            return False
       

def Save(bookid, Member_Email, today, deadline_date, Issued_By):

    if bookid.get() == '':
        msg = 'ENTER A BOOKID'
        messagebox.showerror(title=msg, message=msg)
        return

    if not only_email(Member_Email.get()):
        return

    #First Check wether the book is available
    df = load_log_file()
    print("got hererererer")
    print(bookid.get())
    print("got hererererer")
    df = df.loc[df['Book_ID'] == int(bookid.get())]
    df = df.loc[df['Condition'] == "BORROWED"]

    print(df)
    if(df.shape[0] == 0):
        lst = [uuid.uuid4(),bookid.get(), Member_Email.get(), today, deadline_date, None
            , Issued_By.get(), "", "BORROWED"]
        rr=messagebox.askyesno("Book Library","Ready to Begin CheckOut Process?")
        if (rr==True):
            application_path = os.getcwd()
            with open(application_path + "/logfile.txt","a", newline='') as file:
              Writer=writer(file)
              Writer.writerows([lst])
              file.close()
              messagebox.showinfo("Library","CheckOut Successful")
    else:
        bookID = df['Book_ID'].iloc[0]
        bookCondition = df['Condition'].iloc[0]
        bookComments = df['Comments'].iloc[0]
        msg = "BOOK ID: " + str(bookID) + "\n"
        msg = msg + "CONDITION: " + bookCondition + "\n"
        msg = msg + "COMMENT: " + str(bookComments) + "\n"
        messagebox.showinfo("Library", "CheckOut NOT Successful",)
        messagebox.showinfo("Library", msg, )
        
#clear function to clear the input field
def Clear1(bookid, Member_Email, Issued_By):

   bookid.delete(0,END)
   Member_Email.delete(0,END)
   Issued_By.delete(0,END)


