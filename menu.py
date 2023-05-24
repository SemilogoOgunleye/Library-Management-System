from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk
from idlelib.tooltip import Hovertip
from bookCheckout import only_email, Save, Clear1
from bookReturn import bookreturn, Clear
from bookSearch import searchforbook, getselection
from database import load_log_file, only_letters, only_numbers


def switch_frame(new_frame):
    """
    Switch the current visible frame in the UI.

    Parameters
    ----------
    new_frame : ttk.Frame
        The new frame to display in the UI.
    """
    global current_frame

    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame


def show_main_menu():
    """
    Create the main program menu as a tkinter Frame and
    switches this to the current visible frame.
    """
    main_menu = ttk.Frame(root, padding=50)
    main_menu.grid()
    headingLabel = Label(main_menu, text="MENU", font=('Helvetica bold', 20), fg='black').pack()
    ttk.Button(main_menu, text='Find Book', command=show_find_book_frame).pack()
    ttk.Button(main_menu, text='Check Out Book', command=checkout_book_frame).pack()
    ttk.Button(main_menu, text='Return Book', command=return_books_frame).pack()
    ttk.Button(main_menu, text='Book Availability', command=select_book_frame).pack()
    
    switch_frame(main_menu)


def show_find_book_frame():
    """
    Creates the find book screen as a tkinter Frame and
    switches this to the current visible frame.
    """
    root.title("Find Book Item")
    root.resizable(width=100, height=200)
    root.config(bg="white")

    find_book  = ttk.Frame(root, padding=10)
    find_book.grid()

    ttk.Label(find_book, text="Choose Column:").grid(row=1, column=0)
    selectedCOL = StringVar()
    combobocCOL = ttk.Combobox(find_book, width=10,
                               textvariable=selectedCOL)
    # Adding combobox drop down list
    combobocCOL['values'] = ('Title',
                             'Author',
                             'Genre'
                             )
    combobocCOL.grid(row=2, column=0)
    combobocCOL.current(1)

    tree = ttk.Treeview(find_book)
    tree.grid(row=5, column=0)

    searchVAR = StringVar()
    Entry(find_book, width=20, text="", textvariable=searchVAR, fg="blue").grid(row=3, column=0)
    SearchBook_btn = ttk.Button(find_book, text="Find",command=lambda: searchforbook(tree, searchVAR.get(), selectedCOL.get())).grid(row=4, column=0)  # button

    tree = ttk.Treeview(find_book)
    tree.grid(row=5, column=0)
    GetSelection_btn = ttk.Button(find_book, text="Is the Book Available?",command=lambda: getselection(tree)).grid(row=6, column=0)



    ttk.Button(find_book, text='Back to Main Menu', command=show_main_menu).grid(row=7, column=0)

    switch_frame(find_book)

def checkout_book_frame():
    my_valid = root.register(only_numbers)
    my_valid2 = root.register(only_email) # register
    my_valid3 = root.register(only_letters)
    boolBookAvailable = False
    
    root.title("Borrow Book")
    root.resizable(width=100, height=200)
    root.config(bg="white")
    
    checkout_book  = ttk.Frame(root, padding=10)
    checkout_book.grid()

    
    label0 = Label(checkout_book, text="Book_ID: ")

    label2 = Label(checkout_book, text="Member_Email: ")
    label3 = Label(checkout_book, text="Checkout_Date: ")
    label4 = Label(checkout_book, text="Deadline_Date: ")
    label6 = Label(checkout_book, text="Issued_By: ")


    bookid = Entry(checkout_book, width=30, borderwidth=3, validate="key", validatecommand=(my_valid, '%S'))
    myTip = Hovertip(bookid,'Input numerical values only ')
    Member_Email = Entry(checkout_book, width=30, borderwidth=3, validate="focusout", validatecommand=(my_valid2, '%P'))
    myTip2 = Hovertip(Member_Email,'Email format ')

    Checkout_Date_text = tk.StringVar()
    today = date.today()
    dte = today.strftime("%B %d, %Y")
    Checkout_Date = Label(checkout_book, text = dte)

    Deadline_Date_text = tk.StringVar()
    deadline_date = today + relativedelta(days=7)
    month = deadline_date.strftime("%B %d, %Y")
    Deadline_Date = Label(checkout_book, text = month)


    Issued_By = Entry(checkout_book, width=30, borderwidth=3, validate="key", validatecommand=(my_valid3, '%S'))
    myTip3 = Hovertip(Issued_By,'Input Letters Only ')

    
    save = Button(checkout_book, text="CheckOut", padx=4, pady=10, command=lambda: Save(bookid, Member_Email, today, deadline_date, Issued_By))
    
    clear1 = Button(checkout_book, text="Clear", padx=4, pady=10, command=lambda: Clear1(bookid, Member_Email, Issued_By))




    label0.grid(row=1, column=0)
    label2.grid(row=3, column=0)
    label3.grid(row=4, column=0)
    label4.grid(row=5, column=0)
    label6.grid(row=7, column=0)


    bookid.grid(row=1, column=1)

    Member_Email.grid(row=3, column=1)
    Checkout_Date.grid(row=4, column=1)
    Deadline_Date.grid(row=5, column=1)
    Issued_By.grid(row=7, column=1)
    save.grid(row=9, column=0, columnspan=2)
    clear1.grid(row=9, column=1, columnspan=2)


    ttk.Button(checkout_book, text='Back to Main Menu', command=show_main_menu).grid(row=10, column=0)
    switch_frame(checkout_book)
    
def return_books_frame():
    my_valid = root.register(only_numbers) # restrict user from entering non-numerical values
    my_valid3 = root.register(only_letters)
    root.title("Borrow Return")



    root.resizable(width=100, height=200)
    root.config(bg="white")
    
    return_book  = ttk.Frame(root, padding=10)
    return_book.grid()
    
    #label00 = Label(return_book, text="Member ID: ")
    label0 = Label(return_book, text="Book ID: ")
    label5 = Label(return_book, text="Returned Date: ")
    label8 = Label(return_book, text="Condition: ")
    label9 = Label(return_book, text="Comment: ")
    #UUID_text = tk.StringVar()
    #UUID = Entry(return_book, width=30, borderwidth=3, textvariable=UUID_text, validate="key", validatecommand=(my_valid, '%S'))

    bookid_text = tk.IntVar()
    bookid = Entry(return_book, width=30, borderwidth=3, validate="key", validatecommand=(my_valid, '%S'))
    myTip = Hovertip(bookid,'Book ID is numeric ')

    Returned_Date_text = tk.StringVar()
    today = date.today()
    dte = today.strftime("%B %d, %Y")
    Returned_Date = Label(return_book, text = dte)


    Condition_text = tk.StringVar()
    Condition_text = StringVar()
    Condition = ttk.Combobox(return_book, width=10,
                            textvariable=Condition_text)
    Condition['values'] = ('Good Condition',
                            'Bad Condition'
                            )
    Condition.current(0)

    Accepted_By_text = tk.StringVar()
    Accepted_By = Entry(root, width=30, borderwidth=3,textvariable=Accepted_By_text, validate="key", validatecommand=(my_valid3, '%S'))
    myTip4 = Hovertip(Accepted_By,'Input Letters Only ')

    Comment_text = tk.StringVar()
    Comment = Entry(return_book, width=30, borderwidth=3,textvariable=Comment_text)
    
    bookid_text.set(int("0"))
    bookrtn = Button(return_book, text="Return", padx=2, pady=10, command=lambda: bookreturn(bookid, Condition_text, Comment_text))
    clear = Button(return_book, text="Clear", padx=3, pady=10, command=lambda: Clear(bookid, Accepted_By, Condition, Comment))



    label0.grid(row=2, column=0)
    label5.grid(row=6, column=0)
    label8.grid(row=9, column=0)
    label9.grid(row=10, column=0)
    bookid.grid(row=2, column=1)
    Returned_Date.grid(row=6, column=1)
    Condition.grid(row=9, column=1)

    Comment.grid(row=10, column=1)
    bookrtn.grid(row=12, column=2, columnspan=2)
    clear.place(x = 245, y = 89, height = 43, width = 50)
    
    ttk.Button(return_book, text='Back to Main Menu', command=show_main_menu).grid(row=12, column=0)

    switch_frame(return_book)
    
def select_book_frame():
    root.title("Recommended books")
    root.resizable(width=100, height=200)

    root.config(bg="white")

    select_book  = ttk.Frame(root, padding=10)
    select_book.grid()
    
    tree = ttk.Treeview(select_book)
    for item in tree.get_children():
        tree.delete(item)
    df = load_log_file()
    df = df.loc[df['Condition'] != "BORROWED"]
    df = df.sort_values('Deadline_Date', ascending=True)

    cols = list(df.columns)

    tree["columns"] = cols

    k = 0

    for i in cols:
        tree.column(i, anchor="w")
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert("", index, values=list(row))
    tree.grid(row=2, column=0)


    root.resizable(width=100, height=200)

    root.config(bg="white")

    tree2 = ttk.Treeview(select_book)
    for item in tree2.get_children():
        tree2.delete(item)
    df = load_log_file()
    df = df.loc[df['Condition'] == "BORROWED"]
    df = df.loc[pd.to_datetime(df['Deadline_Date']) < datetime.datetime.now()]
    df = df.sort_values('Deadline_Date', ascending=True)

    cols = list(df.columns)

    tree2["columns"] = cols
    k = 0

    for i in cols:
        tree2.column(i, anchor="w")
        tree2.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree2.insert("", index, values=list(row))
    tree2.grid(row=10, column=0)
    
    ttk.Button(select_book, text='Back to Main Menu', command=show_main_menu).grid(row=11, column=0)

    switch_frame(select_book)

if __name__ == "__main__":
    root = Tk()
    current_frame = None
    
    show_main_menu()
    root.mainloop()