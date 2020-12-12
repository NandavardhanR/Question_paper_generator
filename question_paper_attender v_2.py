import re
import mysql.connector as ms
from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry('400x200')

con = ms.connect(host='localhost', user='root', passwd='root', database='question_paper_generator')
cur = con.cursor()

sel_answers = {}

positive_mark = 4
negative_mark = -1

pad = 10


def retrive_questions():
    query = "select questions from tests where test_id={}".format(test_id_ent.get())
    cur.execute(query)
    questions = cur.fetchall()
    questions = eval(questions[0][0])
    return questions


def retrive_answers():
    questions = retrive_questions()
    c_answers = {}
    for i in questions:
        query = "select answer from questions where question_id={}".format(i)
        cur.execute(query)
        ans = cur.fetchall()
        ans = ans[0][0]
        c_answers[i] = ans
    return c_answers


def show_results():
    questions = retrive_questions()
    correct_answers = retrive_answers()
    marks = 0
    for question in questions:
        if sel_answers[question] == correct_answers[question]:
            marks += positive_mark
        elif sel_answers[question] == 0:
            pass
        elif sel_answers[question] != correct_answers[question] and sel_answers[question] != 0:
            marks += negative_mark
    sel_answers.clear()

    msg = ('you have scored {} out of {}'.format(marks, positive_mark * len(questions)))
    messagebox.showinfo('total score', msg)


def next_question(s, t, n):
    global sel_answers
    questions = retrive_questions()
    if n < len(retrive_questions()) - 1:
        sel_answers[questions[n]] = s.get()

        t.destroy()
        n += 1
        display_questions(n)
    else:
        sel_answers[questions[n]] = s.get()
        t.destroy()
        show_results()


def display_questions(n):
    test = Toplevel(root)
    test.state('zoomed')
    qs = retrive_questions()
    q = PhotoImage(file='questions/q_{}.png'.format(qs[n]))
    a = PhotoImage(file='questions/a_{}.png'.format(qs[n]))
    b = PhotoImage(file='questions/b_{}.png'.format(qs[n]))
    c = PhotoImage(file='questions/c_{}.png'.format(qs[n]))
    d = PhotoImage(file='questions/d_{}.png'.format(qs[n]))

    sel_option = IntVar()
    sel_option.set(0)
    q_lab = Label(test, image=q)
    a_radio = Radiobutton(test, image=a, variable=sel_option, value=1)
    b_radio = Radiobutton(test, image=b, variable=sel_option, value=2)
    c_radio = Radiobutton(test, image=c, variable=sel_option, value=3)
    d_radio = Radiobutton(test, image=d, variable=sel_option, value=4)
    blank_radio = Radiobutton(test, variable=sel_option, value=0)

    q_lab.place(x=pad, y=pad)
    a_radio.place(in_=q_lab, rely=1, y=pad)
    b_radio.place(in_=a_radio, rely=1, y=pad)
    c_radio.place(in_=b_radio, rely=1, y=pad)
    d_radio.place(in_=c_radio, rely=1, y=pad)

    sub_btn = Button(test, text='submit', command=lambda: next_question(sel_option, test, n))

    sub_btn.place(in_=d_radio, rely=1, y=pad)

    test.mainloop()


test_id_lab = Label(root, text='enter your test id here').grid(row=1, column=1,padx=pad,pady=pad)
test_id_ent = Entry(root)
test_id_ent.grid(row=1, column=2,padx=pad,pady=pad)
test_id_btn = Button(root, text='next', command=lambda: display_questions(0)).grid(row=1, column=3,padx=pad,pady=pad)


root.mainloop()
