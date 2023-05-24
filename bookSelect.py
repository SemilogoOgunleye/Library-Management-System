import os
from tkinter import *
from csv import *
from tkinter import ttk
import pandas as pd




root = Tk()

main_lst=[]
boolBookAvailable = False
root.title("Recommended books")
root.resizable(width=100, height=200)

root.config(bg="white")


tree = ttk.Treeview(root)
for item in tree.get_children():
    tree.delete(item)
application_path = os.getcwd()
cols = ['Book_ID','Member_Email','Checkout_Date','Deadline_Date','Returned_Date','Condition','Comments']
read = pd.read_csv(application_path + "/logfile.txt", index_col=False, usecols=cols)
df = pd.DataFrame(read)
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

main_lst=[]
boolBookAvailable = False

root.resizable(width=100, height=200)

root.config(bg="white")

tree = ttk.Treeview(root)
tree = ttk.Treeview(root)
for item in tree.get_children():
    tree.delete(item)
application_path = os.getcwd()
#Book_ID,Member_Email,Checkout_Date,Deadline_Date,Returned_Date,Book_Condition,Comments
cols = ['Book_ID','Member_Email','Checkout_Date','Deadline_Date','Returned_Date','Condition','Comments']
read = pd.read_csv(application_path + "/logfile.txt", index_col=False, usecols=cols)
df = pd.DataFrame(read)
df = df.loc[df['Condition'] == "BORROWED"]
df = df.loc[df['Deadline_Date'] < pd.Timestamp("today").strftime("%d/%m/%Y")]
df = df.sort_values('Deadline_Date', ascending=True)


cols = list(df.columns)

tree["columns"] = cols
k = 0

for i in cols:
    tree.column(i, anchor="w")
    tree.heading(i, text=i, anchor='w')
for index, row in df.iterrows():
    tree.insert("", index, values=list(row))
tree.grid(row=10, column=0)

root.mainloop()