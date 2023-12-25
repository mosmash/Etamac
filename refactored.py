from tkinter import *
from tkinter import ttk
import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime
import os
import time as time_module
import json


# Constants
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
DEFAULT_TIME = 120
TOLERANCE = 0.1
SCORE_FILE = "grind_sheet.txt"
LOG_FILE = "logs.json"
VOICE_SPEED = 120
CHOICES = {'add_sub', 'add', 'sub', 'Hard1DigSub', 'all'}


def get_datetime():
    return datetime.now().strftime(TIME_FORMAT)


class SelectionPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_main_frame()
        self.tkvar = StringVar(self)

        self._create_widgets()

    def _setup_main_frame(self):
        self.mainframe = tk.Frame(self)
        self.mainframe.pack(pady=100, padx=100)

    def _create_widgets(self):
        Label(self.mainframe, text="Choose a test").grid(row=1, column=1)
        Label(self.mainframe, text="Enter test time").grid(row=3, column=1)

        self.time_entry = Entry(self.mainframe)
        self.time_entry.grid(row=4, column=1)

        popupMenu = OptionMenu(self.mainframe, self.tkvar, *CHOICES)
        popupMenu.config(width=20)
        popupMenu.grid(row=2, column=1)

        Button(self.mainframe, text="Submit", width=10, command=self.start_practice).grid(row=3, column=1)

    def start_practice(self):
        test_time = int(self.time_entry.get()) if self.time_entry.get() else DEFAULT_TIME
        app = App(self, test_time, TOLERANCE, self.tkvar.get())
        app.mainloop()


class App(tk.Frame):
    def __init__(self, parent, time, tol, choice):
        super().__init__(parent)
        self.setup_vars(time, tol, choice)
        self.create_widgets()
        self.pack()
        self.update_timer()

    def setup_vars(self, time, tol, choice):
        self.time = time
        self.count = time
        self.scr = 0
        self.tol = tol
        self.choice = choice
        self.start_time = time_module.time()
        self.logs = []

    def create_widgets(self):
        # Define widgets here
        pass

        def next_question(self):
        # Multiplication of 2 digit number by 1-9
            def mul2digit():
                x = random.randint(10, 99)
                y = random.randint(1, 9)
                prompt = '{} x {} ='.format(x, y)
                self.ans = x * y
                return prompt
            # Divison of 3 digit number by 1-9
            def div3digit():
                # make sur number is divisible by y
                x = random.randint(100, 999)
                y = random.randint(1, 9)
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

    def update_timer(self):
        self.count -= 1
        if self.count <= 0:
            self.end_test()
        else:
            self.timer['text'] = "Seconds left: " + str(self.count)
            self.parent.after(1000, self.update_timer)

    def end_test(self):
        messagebox.showinfo("TIME'S UP!", "YOUR SCORE = {}".format(self.scr))
        # Logging and additional actions here...


if __name__ == '__main__':
    app = SelectionPage()
    app.mainloop()
