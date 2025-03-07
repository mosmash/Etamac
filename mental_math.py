import statistics
from tkinter import *
from tkinter import ttk
import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime
import os
import time as time_module
import json
import numpy as np


def calculate_average_times(logs_data):
    # Group logs by question type
    question_types = {}
    for log in logs_data:
        question_type = log["Question Type"]
        if question_type not in question_types:
            question_types[question_type] = []
        question_types[question_type].append(log["Time spent"])

    # Calculate average time for each question type
    average_times = {}
    for question_type, times in question_types.items():
        average_times[question_type] = statistics.mean(times)

    # Sort by average time
    sorted_average_times = sorted(average_times.items(), key=lambda item: item[1], reverse=True)

    return sorted_average_times

def display_average_times(parent, logs_data):
    # Calculate average times
    average_times = calculate_average_times(logs_data)

    # Create a new tkinter window
    window = tk.Toplevel(parent)
    # Create a treeview in the new window
    treeview = ttk.Treeview(window, columns=["Question Type", "Average Time"], show="headings")
    # Set the column identifiers and headings
    treeview.heading("Question Type", text="Question Type")
    treeview.heading("Average Time", text="Average Time")
    # Insert a new item for each average time
    for question_type, average_time in average_times:
        treeview.insert("", "end", values=(question_type, average_time))
    treeview.pack()

def get_datetime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


class SelectionPage(tk.Tk):
    choices_dict = {
    'add_sub': [(['add', 'sub'], 1.0)],
    'add': [(['add'], 1.0)],
    'Hard1DigSub': [(['Hard1DigSub'], 1.0)],
    'sub': [(['sub'], 1.0)],
    'all': [(['add', 'sub', 'mul2digit', 'div3digit', 'mul12'], 0.95), (['mul11'], 0.05)],
    'mul11': [(['mul11'], 1.0)],
    'mul2digit': [(['mul2digit'], 1.0)],
    'div3digit': [(['div3digit'], 1.0)],
    }

    def display_logs(self):
        with open("logs.json", "r") as f:
            logs_data = json.load(f)
        # Create a new tkinter window
        window = tk.Toplevel(self)
        # Create a treeview in the new window
        treeview = ttk.Treeview(window, columns=list(logs_data[0].keys()), show="headings")
        # Set the column identifiers and headings
        for column in logs_data[-1].keys():
            treeview.heading(column, text=column)
        # Insert a new parent item for each log
        for i, log in enumerate(logs_data):
            parent = treeview.insert("", "end", values=list(log.values()))
            # Insert a new child item for each log in the 'logs' array
            for j, log_entry in enumerate(log['logs']):
                treeview.insert(parent, "end", values=('', '', '', log_entry))
        treeview.pack(fill="both", expand=True)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        mainframe = tk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)
        tkvar = StringVar(self)
        choices = self.choices_dict.keys()
        Label(mainframe, text="Choose a test").grid(row=1, column=1)
        Label(mainframe, text="Enter test time").grid(row=3, column=1)
        time_entry = Entry(mainframe)
        time_entry.grid(row=4, column=1)
        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        popupMenu.config(width=20)

        popupMenu.grid(row=2, column=1)

        # Add the "Display Logs" button
        self.display_logs_button = Button(mainframe, text="Display Logs", command=self.display_logs)
        self.display_logs_button.grid(row=5, column=1)

        def start_practice():
            print(tkvar.get())
            time = 120
            if time_entry.get():
                time = int(time_entry.get())  # get the test time from the entry widget

            tol = 0.1 # approximation error tol
            root = Tk()

            choices = self.choices_dict[tkvar.get()]
            app = App(root, time, tol, choices)
            root.mainloop()

        MyButton1 = Button(mainframe, text="Submit", width=10, command=start_practice)
        MyButton1.grid(row=3, column=1)

class App(tk.Frame):
    def __init__(self, parent, time, tol, choices):
        tk.Frame.__init__(self, parent)
        self.time = time
        self.count = time
        self.scr = 0
        self.ans = 5
        self.exact = True
        self.tol = tol

        self.questionType = None
        self.choices = choices

        self.parent = parent
        self.start_time = time_module.time()
        self.logs = []

        self.parent.title("MENTAL MATH QUANT GRIND")
        self.parent.geometry("1000x175")

        self.prompt = Label(self, text="2+3=", bg="gainsboro", width=10,
                        font = ("Arial", 40), anchor = 'e')  # shift text to left: east

        self.answer = Entry(self, font=("Arial", 40), width=20)
        self.answer.bind("<Return>", self.check_answer)


        self.timer = Label(self, text="Seconds left: 1")
        self.score = Label(self, text="score: 0")

        motive = "hi"

        self.motive = Label(self, text=motive, font=("Helvetica", 10, "italic"))

        self.correct_ans = Label(self, font=("Arial", 20))

        self.prompt.grid(row=0)
        self.answer.grid(row=0, column=1)
        self.score.grid(row=1)
        self.timer.grid(row=1, column=1)
        self.correct_ans.grid(row=2)
        self.motive.grid(row=2, column=1)
        self.pack()

        self.onUpdate()

    # Flash window colour
    def flash(self, color):
        self.parent.configure(background=color)
        self.parent.after(300, lambda: self.parent.configure(background='white'))

    def speak(self, prompt):
        #self.engine.say(prompt)
        #self.engine.runAndWait()
        os.system("say -v vicki \"" + prompt + "\" -r 120 &") # & to prevent blocking thread

    def next_question(self):
        # Multiplication of 2 digit number by 1-9
        def mul2digit():
            x = random.randint(10, 99)
            y = random.randint(2, 9)
            prompt = '{} x {} ='.format(x, y)
            self.ans = x * y
            return prompt
        # Divison of 3 digit number by 1-9
        def div3digit():
            # make sur number is divisible by y
            x = random.randint(100, 999)
            y = random.randint(2, 9)
            x = x - x % y
            prompt = '{} / {} ='.format(x, y)
            self.ans = x / y
            return prompt

        def mul9():
            x = random.randint(1, 9)
            prompt = '{} x 9 ='.format(x)
            self.ans = x * 9
            return prompt

        def square5():
            x = random.randint(1, 9)
            prompt = '{}^2 ='.format(10*x + 5)
            self.ans = (10*x + 5)**2
            return prompt
        # ab * 11
        # ab * 10 + ab
        # a*100 b*10 + a*10   b
        def mul11():
            x = random.randint(1, 100)
            prompt = '{} x 11 ='.format(x)
            self.ans = x * 11
            return prompt

        # ba * bc
        # ...
        def mul_firstsame_last10():
            x = random.randint(1, 9)
            y = random.randint(1, 9)
            prompt = '{}{} x {}{} ='.format(x, y, x, 10-y)
            self.ans = (10*x + y) * (10*x + 10-y)
            return prompt


        def square():
            x = random.randint(1, 10)
            prompt = '{}^2 ='.format(x)
            self.ans = x ** 2
            return prompt

        def square_root():
            x = random.randint(1, 100)
            prompt = '\sqrt {} ='.format(x)
            self.ans = x ** (0.5)
            self.exact = False
            return prompt

        def add():
            x = random.randint(1, 100)
            y = random.randint(1, 100)
            prompt = '{} + {} ='.format(x, y)
            self.ans = x + y
            return prompt

        def sub():
            x = random.randint(1, 100)
            y = random.randint(1, 100)
            x, y = sorted([x, y])
            prompt = '{} - {} ='.format(y, x)
            self.ans = y - x
            return prompt

        def Hard1DigSub():
            x = random.randint(1, 9)
            y = random.randint(1, 9)
            x, y = sorted([x, y])
            x = x + random.randint(1, 9) * 10
            x, y = sorted([x, y])
            prompt = '{} - {} ='.format(y, x)
            self.ans = y - x
            return prompt

        def mul12():
            x = random.randint(1, 100)
            prompt = '{} * 12 ='.format(x)
            self.ans = x * 12
            return prompt

        this_fn = locals()
        # Zip the function names and their choice probabilities
        choices, probs = zip(*self.choices)
        # merge all choices into one list
        self.tests = [choice for choice_list in choices for choice in choice_list]
        # Randomly select a question type based on the choice probabilities
        question = np.random.choice([i for i in range(len(self.choices))], p=probs )
        question = random.choice(choices[question])
        #self.tests = [add, sub]

        #self.tests = [sub]
        #self.tests = [mul12]
        #self.tests = [mul9, mul11, square5, \
        #              mul_firstsame_last10, square_root, \
        #              square, square_root, add, sub]

        #self.tests = [square_root, square]
        #self.tests = [square_root]

        #self.tests = [add, square_root]
        self.questionType = question
        #call the function
        prompt = this_fn[question]()
        return prompt

    def check_answer(self, event):
        user_ans = float(self.answer.get().strip())
        diff = abs(user_ans - self.ans)
        print('diff:', diff, '|exact?', self.exact, '| tol:', self.tol, '| my ans:', user_ans)

        if diff == 0 or (not self.exact and diff < self.tol):
            self.flash("green")
            time_spent = time_module.time() - self.start_time
            log = {"Question": self.prompt["text"], "Answer": self.ans, "Time spent": time_spent, "Question Type": self.questionType}
            self.logs.append(log)
            self.correct_ans["text"] = self.prompt["text"] + ('%.3f'% self.ans)
            self.start_time = time_module.time()
            prompt = self.next_question()
            self.prompt["text"] = prompt
            #self.spk(prompt)
            self.scr += 1
            self.answer.delete(0, 'end')
        else:
            self.flash("red")
            self.scr -=2

        self.score["text"] = "score: " + str(self.scr)

    def onUpdate(self):
        # update displayed time
        self.count -=1
        if self.count <= 0:
            messagebox.showinfo("TIME'S UP!", "YOUR SCORE = {}".format(self.scr))
            # Append result to log
            datetime = get_datetime()
            # Sort logs by time spent
            self.logs = sorted(self.logs, key=lambda x: x["Time spent"], reverse=True)
            test_info = {
                "date": datetime,
                "score": self.scr,
                "time": self.time,
                "tests": self.tests,
                "logs": self.logs
            }
             # Create a new tkinter window
            window = tk.Toplevel(self.parent)
            # Create a treeview in the new window
            treeview = ttk.Treeview(window, columns=list(test_info["logs"][0].keys()), show="headings")
            # Set the column identifiers and headings
            for column in test_info["logs"][0].keys():
                treeview.heading(column, text=column)
            # Insert a new item for each log
            for log in test_info["logs"]:
                treeview.insert("", "end", values=list(log.values()))
            treeview.pack()
            if not os.path.isfile("logs.json"):
                logs_data = []
            else:
                # If file exists, load the existing data
                with open("logs.json", "r") as f:
                    logs_data = json.load(f)
            display_average_times(self.parent, self.logs)
            # Append the new data
            logs_data.append(test_info)
            # Write the data back to the file
            with open("logs.json", "w") as f:
                json.dump(logs_data, f)

        else:
            self.timer['text'] = "Seconds left: " + str(self.count)
            # schedule timer to call myself after 1 second
            self.parent.after(1000, self.onUpdate)

if __name__ == '__main__':
    # https://pythonspot.com/tk-dropdown-example/
    #root = Tk()
    #time = 180

    #tol = 0.1 # approximation error tol

    #app = App(root, time, tol)
    #root.mainloop()

    ## LOGGING
    # LEGACY
    #datetime = get_datetime()
    #log_score = "grind_sheet.txt"
    #log = datetime + " | " + "score = " + str(app.scr) + " | " + "time = " \
    #      + str(time) + " | " + "tests = " + " ;".join([fn.__name__ for fn in app.tests]) \
    #      + "\n"

    #print("Result >>", log)
    #with open(log_score, "a") as f:
    #    f.write(log)

    app = SelectionPage()
    app.mainloop()


