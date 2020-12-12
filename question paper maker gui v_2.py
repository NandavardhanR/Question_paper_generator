import mysql.connector as ms
import random
from tkinter import *
from tkinter import messagebox


classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
subjects = ['Maths', 'Physics', 'Chemistry']
topics_maths = ['matrices', 'intergral']
topics_physics = ['optics', 'current electricity']
topics_chemistry = ['amines', 'polymers']
difficulties = ['easy', 'medium', 'hard']
subject_index = {subjects[0]: 41, subjects[1]: 42, subjects[2]: 43}
difficulty_index = {difficulties[0]: 1, difficulties[1]: 2, difficulties[2]: 3}
topics = ['']
questions = []
test_id = 0
pad = 10

con = ms.connect(host='localhost', user='root', passwd='root', database='question_paper_generator')
cur = con.cursor()

root = Tk()
root.geometry('768x480')


def sel_topic(event):
    topic_sel.set('')
    d = {'Maths': topics_maths, 'Physics': topics_physics, 'Chemistry': topics_chemistry}
    topic_dropdown.children["menu"].delete(0, "end")
    a = d[sub_sel.get()]
    for i in a:
        topic_dropdown.children["menu"].add_command(label=i, command=lambda x=i: topic_sel.set(x))


def get_data():
    selected_class = int(class_sel.get())
    selected_subject = subject_index[sub_sel.get()]
    selected_topic = topic_sel.get()
    if selected_topic in topics_maths:
        selected_topic = topics_maths.index(selected_topic) + 1
    if selected_topic in topics_physics:
        selected_topic = topics_physics.index(selected_topic) + 1
    if selected_topic in topics_chemistry:
        selected_topic = topics_chemistry.index(selected_topic) + 1
    selected_difficulty = difficulty_index[difficulty_sel.get()]
    return([selected_class, selected_subject, selected_topic, selected_difficulty])


def retrive_data_sql():
    query = "select question_id from questions where class = {} and sub = {} and topic = {} and difficulty = {}".format(*get_data())
    cur.execute(query)
    data = cur.fetchall()
    data = random.sample(data, int(no_questions_sel.get()))
    for i in data:
        questions.append(i[0])
    print(questions)
    messagebox.showinfo('questions have beeen added', '{} question have been added to the question paper'.format(no_questions_sel.get()))
    class_sel.set('')
    sub_sel.set('')
    topic_sel.set('')
    difficulty_sel.set('')
    no_questions_sel.set('')


def display_questions(n):
    test = Toplevel(root)
    test.state('zoomed')

    q = PhotoImage(file='questions/q_{}.png'.format(questions[n]))
    a = PhotoImage(file='questions/a_{}.png'.format(questions[n]))
    b = PhotoImage(file='questions/b_{}.png'.format(questions[n]))
    c = PhotoImage(file='questions/c_{}.png'.format(questions[n]))
    d = PhotoImage(file='questions/d_{}.png'.format(questions[n]))

    q_lab = Label(test, image=q)
    a_lab = Label(test, image=a)
    b_lab = Label(test, image=b)
    c_lab = Label(test, image=c)
    d_lab = Label(test, image=d)

    q_lab.place(x=pad, y=pad)
    a_lab.place(in_=q_lab, rely=1, y=pad, relx=0, x=0, anchor='nw')
    b_lab.place(in_=a_lab, rely=1, y=pad, relx=0, x=0, anchor='nw')
    c_lab.place(in_=b_lab, rely=1, y=pad, relx=0, x=0, anchor='nw')
    d_lab.place(in_=c_lab, rely=1, y=pad, relx=0, x=0, anchor='nw')

    next_btn = Button(test, text='next', command=lambda: next_question(test, n))
    next_btn.place(in_=d_lab, rely=1, y=pad)
    test.mainloop()


def next_question(t, n):
    if n < len(questions) - 1:
        t.destroy()
        n += 1
        display_questions(n)
    else:
        t.destroy()
        messagebox.showinfo('questions paper code', 'question paper code is:{}'.format(test_id))


def submit():
    global test_id
    last_test_id = 0
    query = "select test_id from tests"
    cur.execute(query)
    test_ids = cur.fetchall()
    last_test_id = int(test_ids[-1][0])
    test_id = last_test_id + 1
    query = "insert into tests value({},{});".format(test_id, "'" + str(questions) + "'")
    cur.execute(query)
    con.commit()
    display_questions(0)


# class selection
class_sel = StringVar()
class_lab = Label(root, text='Class')
class_lab.grid(row=1, column=1, padx=pad, pady=pad)
class_dropdown = OptionMenu(root, class_sel, *classes)
class_dropdown.grid(row=1, column=2, padx=pad, pady=pad)


# subject selection
sub_sel = StringVar()
sub_lab = Label(root, text='Subject')
sub_lab.grid(row=2, column=1)
sub_dropdown = OptionMenu(root, sub_sel, *subjects, command=sel_topic)
sub_dropdown.grid(row=2, column=2, padx=pad, pady=pad)


# topic selection according to the subject selected
topic_sel = StringVar()
topic_lab = Label(root, text='topic')
topic_lab.grid(row=3, column=1, padx=pad, pady=pad)
topic_dropdown = OptionMenu(root, topic_sel, *topics)
topic_dropdown.grid(row=3, column=2, padx=pad, pady=pad)

# difficulty selection
difficulty_sel = StringVar()
difficulty_lab = Label(root, text='difficulty level')
difficulty_lab.grid(row=4, column=1, padx=pad, pady=pad)
difficulty_dropdown = OptionMenu(root, difficulty_sel, *difficulties)
difficulty_dropdown.grid(row=4, column=2, padx=pad, pady=pad)


no_questions_sel = StringVar()
no_questions_lab = Label(root, text='enter number of question:').grid(row=5, column=1, padx=pad, pady=pad)
no_questions = Entry(root, textvariable=no_questions_sel).grid(row=5, column=2, padx=pad, pady=pad)


add_btn = Button(root, text='add questions', command=retrive_data_sql).grid(row=6, column=1, padx=pad, pady=pad)

submit_btn = Button(root, text='submit', command=submit).grid(row=6, column=2, padx=pad, pady=pad)

root.mainloop()
