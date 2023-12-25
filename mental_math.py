from tkinter import *
from tkinter import ttk
import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime
import os
import time as time_module
import json


def get_datetime():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


class SelectionPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        mainframe = tk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)
        tkvar = StringVar(self)
        choices = {'add_sub', 'add', 'sub', 'Hard1DigSub', 'all', 'div3digit'}
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
            choices_dict = {'add_sub': ['add', 'sub'],
                            'add': ['add'],
                            'Hard1DigSub': ['Hard1DigSub'],
                            'sub': ['sub'],
                            'all': ['add', 'sub', 'mul2digit', 'div3digit'],
                            'div3digit': ['div3digit'],}

            app = App(root, time, tol, choices_dict[tkvar.get()])
            root.mainloop()

        MyButton1 = Button(mainframe, text="Submit", width=10, command=start_practice)
        MyButton1.grid(row=3, column=1)

    def display_logs(self):
        with open("logs.json", "r") as f:
            logs_data = json.load(f)
        # Create a new tkinter window
        window = tk.Toplevel(self)
        # Create a treeview in the new window
        treeview = ttk.Treeview(window, columns=list(logs_data), show="headings")
        # Set the column identifiers and headings
        for column in logs_data.keys():
            treeview.heading(column, text=column)
        # Insert a new item for each log
        for log in logs_data:
            treeview.insert("", "end", values=list(log.values()))
        treeview.pack(fill="both", expand=True)

class App(tk.Frame):
    def __init__(self, parent, time, tol, choices):
        tk.Frame.__init__(self, parent)
        self.time = time
        self.count = time
        self.scr = 0
        self.ans = 5
        self.exact = True
        self.tol = tol

        self.choices = choices

        self.parent = parent
        self.start_time = time_module.time()
        self.logs = []

        self.parent.title("MENTAL MATH QUANT GRIND")
        self.parent.geometry("700x130")

        self.prompt = Label(self, text="2+3=", bg="gainsboro", width=10,
                        font = ("Roman", 40), anchor = 'e')  # shift text to left: east

        self.answer = Entry(self, font=("Roman", 40), width=20)
        self.answer.bind("<Return>", self.check_answer)


        self.timer = Label(self, text="Seconds left: 1")
        self.score = Label(self, text="score: 0")

        motive = "hi"

        self.motive = Label(self, text=motive, font=("Helvetica", 10, "italic"))

        self.correct_ans = Label(self, font=("Roman", 20))

        self.prompt.grid(row=0)
        self.answer.grid(row=0, column=1)
        self.score.grid(row=1)
        self.timer.grid(row=1, column=1)
        self.correct_ans.grid(row=2)
        self.motive.grid(row=2, column=1)
        self.pack()

        self.onUpdate()

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
        self.tests = [this_fn[i] for i in self.choices]
        #self.tests = [add, sub]

        #self.tests = [sub]
        #self.tests = [mul12]
        #self.tests = [mul9, mul11, square5, \
        #              mul_firstsame_last10, square_root, \
        #              square, square_root, add, sub]

        #self.tests = [square_root, square]
        #self.tests = [square_root]

        #self.tests = [add, square_root]


        return random.choice(self.tests)()

    def check_answer(self, event):
        user_ans = float(self.answer.get().strip())
        diff = abs(user_ans - self.ans)
        print('diff:', diff, '|exact?', self.exact, '| tol:', self.tol, '| my ans:', user_ans)

        if diff == 0 or (not self.exact and diff < self.tol):
            time_spent = time_module.time() - self.start_time
            log = {"Question": self.prompt["text"], "Answer": self.ans, "Time spent": time_spent }
            self.logs.append(log)
            self.correct_ans["text"] = self.prompt["text"] + ('%.3f'% self.ans)
            self.start_time = time_module.time()
            prompt = self.next_question()
            self.prompt["text"] = prompt
            #self.speak(prompt)
            self.scr += 1
            self.answer.delete(0, 'end')
        else:
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
                "tests": [fn.__name__ for fn in self.tests],
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


