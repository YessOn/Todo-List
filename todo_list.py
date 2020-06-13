from tkinter import *
import re
from camelcase import CamelCase

# Root window
root = Tk()
root.configure(bg="#EEE")
root.title("ToDo List")
root.geometry("675x445")
root.resizable(0, 0)

# My Tasks
tasks = []
# Generate My Previous Tasks from a log file
with open("log.txt", "r") as f:
	txt_tasks = f.readline()
	for task in txt_tasks.split(","):
		if task.strip() != "":
			tasks.append(task)

# Util functions
def update_listbox():
	clear_listbox()
	for i in tasks:
		tasks_listbox.insert("end", i)

def clear_listbox():
	tasks_listbox.delete(0, "end")

def add_task():
	task = text_input.get()
	if task.strip() != "":
		tasks.append(CamelCase().hump(task))
		update_listbox()
	else:
		display_n_of_tasks["text"] = "Please enter a task!"
	text_input.delete(0, "end")

def delete_one():
	task = tasks_listbox.get("active")
	if task in tasks:
		tasks.remove(task)
	update_listbox()

def sort_asc():
	tasks.sort()
	update_listbox()

def sort_desc():
	tasks.sort()
	tasks.reverse()
	update_listbox()

def n_of_tasks():
	number_of_tasks = len(tasks)
	msg = f"Number of tasks: {number_of_tasks}"
	display_n_of_tasks["text"]=msg

def text_input_on_click(event):
    text_input.delete(0, END)
    text_input.unbind('<Button-1>', on_click_text_input_id)
def search_input_on_click(event):
    search_input.delete(0, END)
    search_input.unbind('<Button-1>', on_click_search_input_id)

def search():
	if search_input.get().strip() != "":
		found_tasks = [task for task in tasks if re.search(search_input.get(), task, re.I)]
		clear_listbox()
		for task in found_tasks: tasks_listbox.insert(END, task)
	else: update_listbox()
# Label Widgets
title = Label(root, text="My To-Do List", fg="#E2252B",bg="#EEE", font="Verdana 30 bold")
title.grid(row=0,column=0, pady=(6, 20))

display_n_of_tasks = Label(root, text="", font="Tahoma 16", bg="#EEE")
display_n_of_tasks.grid(row=2,column=0, columnspan=2, padx=(16, 16))

# Button Widgets
add_task_btn = Button(root, text="⊕ Add", relief=GROOVE, width="14", font="Tahoma 16", fg="white", bg="#1890FF", activebackground="#1890FF", activeforeground="white", command=add_task)
add_task_btn.grid(row=1,column=2)

Button(root, text="␥ Delete", relief=GROOVE, width="14", font="Tahoma 16", fg="white", bg="#fb7c42", activebackground="#fb7c42", activeforeground="white", command=delete_one).grid(row=3,column=2)

sort_asc_btn = Button(root, text="▲ Sort (ASC)", relief=GROOVE, width="14", font="Tahoma 16", fg="white", bg="#5fbc5e", activebackground="#5fbc5e", activeforeground="white", command=sort_asc)
sort_asc_btn.grid(row=5,column=2)

sort_desc_btn = Button(root, text="▼ Sort (DESC)", relief=GROOVE, width="14", font="Tahoma 16", fg="white", bg="#5fbc5e", activebackground="#5fbc5e", activeforeground="white", command=sort_desc)
sort_desc_btn.grid(row=7,column=2)

n_of_tasks_btn = Button(root, text="＃ Tasks Number", relief=GROOVE, width="14", font="Tahoma 16", fg="white", bg="#f0c022", activebackground="#f0c022", activeforeground="white", command=n_of_tasks)
n_of_tasks_btn.grid(row=9,column=2)

# Search panel
search_input = Entry(root, relief=GROOVE, width="17", font="Tahoma 14")
search_input.grid(row=0,column=2)
search_input.insert(0, "Search!")
on_click_search_input_id = search_input.bind('<Button-1>', search_input_on_click)
Button(root, text="⌕", relief=GROOVE, font="Tahoma 12", height="1", command=search).grid(row=0,column=2, padx=(152, 0))

# Inputs Widegts
text_input = Entry(root, relief=FLAT, width="39", bd="8", font="Tahoma 16")
text_input.grid(row=1,column=0,columnspan=2, padx=(16, 16))
text_input.insert(0, "Title your task")
on_click_text_input_id = text_input.bind('<Button-1>', text_input_on_click)

tasks_listbox = Listbox(root, width="40", relief=FLAT, bd="4", font="Tahoma 16")
tasks_listbox.grid(row=3,column=0, columnspan=2, rowspan=9, padx=(16, 16))

# Just before closing Save all the tasks in a log file
def on_closing():
	with open("log.txt", "w") as f: f.write(",".join(tasks))
	root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

# mainloop function
root.mainloop()
