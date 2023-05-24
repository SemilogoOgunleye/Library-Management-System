import os
from tkinter import *
from csv import *
import tkinter as tk
from tkinter import Label, ttk, messagebox
from tkinter import Label
import pandas as pd
from idlelib.tooltip import Hovertip
from datetime import date
from database import only_letters
from database import only_numbers



def bookreturn(bookid, Condition_text, Comment_text):

        rr = messagebox.askyesno("Library", "Ready to Begin Book return Process?")
        if (rr == False):
            return
        
        application_path = os.getcwd()
        with open(application_path + "/logfile.txt", 'r') as fr:
            # reading line by line
            lines = fr.readlines()

            recdata=[]
            lst=[]
            book_id_search = f',{bookid.get()},'

            for line in lines:
                if (line.find(book_id_search) > -1 and line.find('BORROWED') > -1):
                    recdata = line.split(",")
                    lst = [recdata[0]  # uuid.uuid4(),
                        , recdata[1]  # bookid.get(),
                        , recdata[2]  # Member_Email.get(),
                        , recdata[3]  # Checkout_Date.get(),
                        , recdata[4]  # Deadline_Date.get(),
                        , recdata[5]  # Returned_Date.get()
                        , recdata[6]  # Issued_By.get()
                        , recdata[7]  # Accepted_By.get()
                        , Condition_text.get()  # "BORROWED"
                        , Comment_text.get()  # "BORROWED"
                           ]
            if lst == []:
                messagebox.showerror(title="ERROR", message="BOOK NOT OUT ON LOAN.")
                return

            # opening in writing mode
            with open(application_path + "/logfile.txt", 'w') as fw:
                for line in lines:
                    if (line.find(book_id_search) > -1 and line.find('BORROWED') > -1):
                        fw.write(','.join(lst) + '\n')
                    else:
                        fw.write(line)
                
                fw.write('\n')
                fw.close()       
            fr.close()
        print("Deleted")

        messagebox.showinfo("Library", "Return Successful")



def Clear(bookid, Accepted_By, Condition, Comment):
   bookid.delete(0,END)
   Accepted_By.delete(0,END)
   Condition.delete(0, END)
   Comment.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    my_valid = root.register(only_numbers) # restrict user from entering non-numerical values
    my_valid3 = root.register(only_letters)
    main_lst=[]
    boolBookAvailable = False
    root.title("Borrow Return")
    main_lst=[]


    root.resizable(width=100, height=200)
    root.config(bg="white")
    label00 = Label(root, text="Member ID: ")
    label0 = Label(root, text="Book ID: ")


    label5 = Label(root, text="Returned Date: ")
    label7 = Label(root, text="Accepted By: ")
    label8 = Label(root, text="Condition: ")
    label9 = Label(root, text="Comment: ")
    UUID_text = tk.StringVar()
    UUID = Entry(root, width=30, borderwidth=3, textvariable=UUID_text, validate="key", validatecommand=(my_valid, '%S'))

    bookid_text = tk.IntVar()
    bookid = Entry(root, width=30, borderwidth=3, validate="key", validatecommand=(my_valid, '%S'))
    myTip = Hovertip(bookid,'Book ID is numeric ')


    Returned_Date_text = tk.StringVar()
    today = date.today()
    date = today.strftime("%B %d, %Y")
    Returned_Date = Label(text = date)


    Accepted_By_text = tk.StringVar()
    Accepted_By = Entry(root, width=30, borderwidth=3,textvariable=Accepted_By_text, validate="key", validatecommand=(my_valid3, '%S'))
    myTip4 = Hovertip(Accepted_By,'Input Letters Only ')

    Condition_text = tk.StringVar()
    Condition_text = StringVar()
    Condition = ttk.Combobox(root, width=10,
                            textvariable=Condition_text)
    # Adding combobox drop down list
    Condition['values'] = ('Good Condition',
                            'Bad Condition'
                            )
    Condition.current(0)


    Comment_text = tk.StringVar()
    Comment = Entry(root, width=30, borderwidth=3,textvariable=Comment_text)

def GetCheckOutDetails(bookid):

    #First Check whether the book is available
    application_path = os.getcwd()
    cols = ['Book_ID','Member_Email','Checkout_Date','Deadline_Date','Returned_Date','Condition','Comments']
    read = pd.read_csv(application_path + "/logfile.txt", index_col=False, usecols=cols)
    df = pd.DataFrame(read)
    
    # df = pd.DataFrame(read)
    print("got hererererer")
    varbookid=bookid.get()
    print(varbookid)
    print("got hererererer")
    df = df.loc[df['Book_ID'] == bookid.get()]
    df = df.loc[df['Condition'] == "BORROWED"]

    print(df)
    if(df.size >= 1):
        returnDate = df['Returned_Date'].iloc[0]
        bookID = df['Book_ID'].iloc[0]
        # Book_Condition,Comments
        bookCondition = df['Condition'].iloc[0]
        booComments = df['Comments'].iloc[0]
        msg = "BOOK ID: " + str(bookID) + "\n"
        msg = msg + "RETURNED DATE: " + returnDate + "\n"
        msg = msg + "CONDITION: " + bookCondition + "\n"
        msg = msg + "COMMENT: " + booComments + "\n"
        messagebox.showinfo("Library", "CheckOut NOT Successful",)
        messagebox.showinfo("Library", msg, )
#ID,Book_ID,Member_Email,Checkout_Date,Deadline_Date,Returned_Date,Issued_By,Accepted_By,Book_Condition,Comments
        UUID_text.set(df['ID'].iloc[0])
        bookid_text.set(df['Book_ID'].iloc[0])
        Returned_Date_text.set(df['Returned_Date'].iloc[0])
        Accepted_By_text.set(df['Accepted_By'].iloc[0])
        Condition_text.set(df['Condition'].iloc[0])

        Comment_text.set(df['Comments'].iloc[0])
    else:
        messagebox.showinfo("Library", "Book ID: "+ varbookid + "  already Returned", )
        
