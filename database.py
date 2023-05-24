import os
import pandas as pd
from tkinter import *
from csv import *


def open_log_file():
    pass

def open_Book_Info_file():
    pass

def load_book_db():
    application_path = os.getcwd()
    read = pd.read_csv(application_path + "/Book_Info.txt", usecols=['ID','Genre','Title'
        ,'Author','Purchase_Price','Purchase_Date'],index_col=False)
    df = pd.DataFrame(read)

    return df


def load_log_file():
    application_path = os.getcwd()
    dtypes = {
        'ID': str,
        'Book_ID': int,
        'Member_Email': str,
        'Checkout_Date': str,
        'Deadline_Date': str,
        'Returned_Date': str,
        'Issued_By': str,
        'Accepted_By': str,
        'Condition': str,
        'Comments': str
    }
    df = pd.read_csv(application_path + "/logfile.txt", index_col=False, dtype=dtypes)

    return df


def is_book_available(book_id):
    log_df = load_log_file()

    log_df = log_df.loc[(log_df['Condition'] == "BORROWED") & (log_df['Book_ID'] == book_id)]

    return log_df.size == 0

#function to restrict inputs that is non-numerical entered by the user 
def only_numbers(char):
    return char.isdigit()

#function to restrict inputs that is not letters from the alphabet
def only_letters(char):
    return char.isalpha()   
    

