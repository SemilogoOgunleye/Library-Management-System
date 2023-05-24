from tkinter import *
from csv import *
from tkinter import messagebox
import pandas as pd
from database import load_log_file, load_book_db


def getselection(tree):
    selecteditem=tree.focus()
    details =tree.item(selecteditem)
    print(selecteditem)


    df = load_log_file()
    print("got hererererer")
    df = df.loc[df['Condition'] == "BORROWED"]
    print(df)
    df = df.sort_values('Condition', ascending=True)

    if (df.size < 1):
        #proceed to checkout
        boolBookAvailable=True
        print("NOT FOUND")
        msg = "ID: " + str(details['values'][0]) + "\n"
        msg = msg + "GENRE: " + str(details['values'][1]) + "\n"
        msg = msg + "TITLE: " + str(details['values'][2]) + "\n"
        msg = msg + "AUTHOR: " + str(details['values'][3]) + "\n"
        msg = msg + "PURCHASE_PRICE: " + str(details['values'][4]) + "\n"
        msg = msg + "PURCHASE_DATE: " + str(details['values'][5]) + "\n"
        msg = msg + ":::::::::::::::::::::::::::::::::::::::::::::::" + "\n"
        msg = msg + "The Book  is Available " + "\n"
        msg = msg + ":::::::::::::::::::::::::::::::::::::::::::::::" + "\n"
        msg = msg + "TranDate: " + str(pd.Timestamp("today").strftime("%d/%m/%Y"))+ "\n"

        res = messagebox.showinfo("LIBRARY", msg, )

    if (df.size >= 1):
        boolBookAvailable = True

        print("FOUND")
        df = df.sort_values('Returned_Date', ascending=False)
        returnDate=df['Returned_Date'].iloc[0]
        bookID = df['Book_ID'].iloc[0]
        bookCondition= df['Condition'].iloc[0]
        bookComments = df['Comments'].iloc[0]
        msg = "BOOK ID: " + str(bookID)+ "\n"
        msg = msg + "CONDITION: " + bookCondition  + "\n"
        msg = msg + "COMMENT: " + str(bookComments) + "\n"

        msg = msg + ":::::::::::::::::::::::::::::::::::::::::::::::" + "\n"

        msg = msg + "TranDate: "+str(pd.Timestamp("today").strftime("%d/%m/%Y"))+ "\n"
        msg = msg + ":::::::::::::::::::::::::::::::::::::::::::::::" + "\n"

        print(msg)
        res = messagebox.showinfo("LIBRARY",msg,)


def search_books(df, term, col):
    df = df.loc[df[col].str.contains(term)]
    df = df.sort_values('ID', ascending=True)

    return df


def refresh_tree(tree, df):
    # CLear the tree
    for item in tree.get_children():
        tree.delete(item)

    cols = list(df.columns)
    tree["columns"] = cols
    k=0

    for i in cols:
        tree.column(i, anchor="w")
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert(  "",index,values=list(row))
    # tree.grid(row=2, column=0)


def searchforbook(tree, term, col):
    print("search string  in the dictionanary of columns  :::" , col)

    book_df = load_book_db()
    filtered_df = search_books(book_df, term, col)

    refresh_tree(tree, filtered_df)


