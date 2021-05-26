from tkinter import *
from tkinter import ttk
from time import *
from random import *
from enum import Enum
import math


class OPERATOR(Enum):
    INVALID = -1
    NONE = 0
    NUM = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    POWER = 6


class Token():
    type = OPERATOR.NUM
    value = 0

    def numeric(self, n):
        self.type = OPERATOR.NUM
        self.value = n
        return self

    def operator(self, o):
        self.type = o
        return self

    def brackets(self, n):
        self.value = n
        return self

    def getPriority(self):
        typePriorities = {OPERATOR.PLUS: 0,
                          OPERATOR.MINUS: 0,
                          OPERATOR.MULTIPLY: 1,
                          OPERATOR.DIVIDE: 2,
                          OPERATOR.POWER: 3}
        return self.value * 256 + typePriorities[self.type]

    def operatorAsString(self):
        lookup = {OPERATOR.INVALID: "invalid",
                  OPERATOR.NONE: "none",
                  OPERATOR.NUM: "number",
                  OPERATOR.PLUS: "+",
                  OPERATOR.MINUS: "-",
                  OPERATOR.MULTIPLY: "*",
                  OPERATOR.DIVIDE: "/",
                  OPERATOR.POWER: "^"}
        return lookup[self.type]

    def print(self):
        if self.type == OPERATOR.NUM:
            print("Number: " + str(self.value))
        else:
            print("OP: " + self.operatorAsString())


class StringParser:
    string = ""
    pointer = 0
    brackets = 0
    expectNumeric = True
    error = False

    def __init__(self, string):
        self.string = string
        self.pointer = 0
        self.brackets = 0
        self.expectNumeric = True

    def NextToken(self):
        if self.error:
            return Token().operator(OPERATOR.INVALID)
        substring = ""
        firstCharacter = True
        isFloat = False
        for i in range(self.pointer, len(self.string)):
            C = self.string[i]
            if firstCharacter:
                if C == " ":
                    pass
                elif C == "(":
                    self.brackets += 1
                elif C == ")":
                    self.brackets -= 1
                    if self.brackets < 0:
                        self.error = "Bracket counting error."
                        return Token().operator(OPERATOR.INVALID)
                elif not self.expectNumeric:
                    lookup = {"+": OPERATOR.PLUS,
                              "-": OPERATOR.MINUS,
                              "*": OPERATOR.MULTIPLY,
                              "/": OPERATOR.DIVIDE,
                              "^": OPERATOR.POWER}
                    if not C in lookup:
                        self.error = "Invalid operator at character: " + str(i)
                        return Token().operator(OPERATOR.INVALID)
                    self.expectNumeric = True
                    self.pointer = i + 1;
                    return Token().operator(lookup[C]).brackets(self.brackets)
                elif C == "-":
                    if i == len(self.string) - 1 or not self.string[i + 1] in "1234567890.":
                        self.error = "Stray minus sign at character: " + str(i)
                        return Token().operator(OPERATOR.INVALID)
                    substring += C
                    firstCharacter = False
                    continue
                elif not C in "1234567890.":
                    self.error = "Expected number at character: " + str(i)
                    return Token().operator(OPERATOR.INVALID)
                else:
                    firstCharacter = False
            if not firstCharacter:
                if C == ".":
                    isFloat = True
                    substring += C
                elif C in "1234567890":
                    substring += C
                else:
                    i -= 1
                    break
        if firstCharacter:
            if self.brackets != 0:
                self.error = "Bracket counting error."
                return Token().operator(OPERATOR.INVALID)
            return Token().operator(OPERATOR.NONE)
        self.pointer = i + 1
        self.expectNumeric = False
        try:
            if isFloat:
                return Token().numeric(float(substring))
            else:
                return Token().numeric(int(substring))
        except ValueError:
            print(substring)
            self.error = "Expected number at character: " + str(i)
            return Token().operator(OPERATOR.INVALID)


class Expression:
    def __init__(self, string):
        RPN = ""
        opStack = []
        evaluationStack = []

        def evaluate(operator):
            b = evaluationStack.pop()
            a = evaluationStack.pop()
            c = 0
            if operator == OPERATOR.PLUS:
                c = a + b
            if operator == OPERATOR.MINUS:
                c = a - b
            if operator == OPERATOR.MULTIPLY:
                c = a * b
            if operator == OPERATOR.DIVIDE:
                c = a / b
            if operator == OPERATOR.POWER:
                c = pow(a, b)
            evaluationStack.append(c)

        s = StringParser(string)
        while True:
            token = s.NextToken()
            if token.type == OPERATOR.INVALID:
                print("String parse error: " + s.error)
                quit()
            elif token.type == OPERATOR.NONE:
                break
            elif token.type == OPERATOR.NUM:
                evaluationStack.append(token.value)
                RPN += str(token.value) + " "
            else:
                while True:
                    if len(opStack) == 0:
                        opStack.append(token)
                        break
                    if token.getPriority() <= opStack[
                        -1].getPriority():
                        op = opStack.pop()
                        evaluate(op.type)
                        RPN += op.operatorAsString() + " "
                    else:
                        opStack.append(token)
                        break
        while len(opStack) != 0:
            op = opStack.pop()
            evaluate(op.type)
            RPN += op.operatorAsString() + " "
        # self.write(evaluationStack[0])
        global ans
        ans = (evaluationStack[0])


class Load(Tk):
    def __init__(self):
        super().__init__()

        self.width = 900
        self.height = 600
        self.bg = "#343949"

        self.geometry("900x600")
        self.title("Numeric Calculator")
        self.config(bg=self.bg)

        self.resizable(0, 0)
        self.iconbitmap(
            "Icon.ico")

        self.Draw()

    def Draw(self):
        self.image = PhotoImage(
            file="Icon.png")

        self.place = Label(
            self,
            image=self.image,
            bg=self.bg)
        self.place.place(x=self.width / 3, y=self.height / 6 - 50)

        self.Title = Label(
            self,
            text="Calculator",
            font=("Courier New", 20, "bold"),
            bg=self.bg,
            fg="#cccccc")
        self.Title.place(x=self.width / 2.5, y=self.height / 2 + 50)

        self.loading()

    def loading(self):
        self.progressbar = ttk.Progressbar(
            self, orient=HORIZONTAL, length=200, mode='determinate')
        self.progressbar.place(x=350, y=550)
        self.progressbar["maximum"] = 2

        for i in range(3):
            sleep(1)
            self.progressbar["value"] = i
            self.progressbar.update()
        self.kill()
        self.next()

    def kill(self):
        sleep(2)
        self.destroy()

    def next(self):
        main = Main()
        main.mainloop()


class Main(Tk):
    def __init__(self):
        super().__init__()

        self.bg = "#343949"

        self.geometry("900x600")
        self.title("Numeric Calculator")
        self.config(bg=self.bg)

        self.resizable(0, 0)
        self.iconbitmap("Icon.ico")

        self.func = functions()

        self.Draw()
        self.Draw_Basic()
        global f
        f = open('Output.txt', 'w')

    def Draw(self):
        self.claculation = Entry(
            self,
            width=18,
            bg=self.bg,
            fg="white",
            font=("Courier New", 15, "bold"),
            textvariable=self.func.equation)
        self.claculation.place(x=450, y=10)

        self.typeArea = LabelFrame(
            self,
            width=175,
            height=900,
            bg=self.bg,
            fg="white")
        self.typeArea.place(x=0, y=0)

        self.basic = Button(
            self.typeArea,
            text="Basic",
            width=20,
            height=1,
            bg=self.bg,
            fg="white",
            font=("Courier New", 10, "bold"),
            command=self.Draw_Basic)
        self.basic.place(x=0, y=0)

        self.MoreComming = Label(
            self.typeArea,
            text="-More Coming-",
            width=20,
            height=1,
            bg=self.bg,
            fg="white",
            font=("Courier New", 10, "bold"))
        self.MoreComming.place(x=0, y=300)

        self.History = LabelFrame(
            self,
            width=175,
            height=900,
            font=("Courier New", 15, "bold"),
            bg=self.bg,
            fg="white")
        self.History.place(x=725, y=0)

        self.Hist_num = Label(
            self.History,
            text="",
            bg=self.bg,
            fg="white",
            font=("Courier New", 15, "bold"))
        self.Hist_num.place(x=0, y=40)

        self.label = Label(
            self.History,
            text="History",
            font=("Courier New", 15, "bold"),
            bg=self.bg,
            fg="white",
            padx=40)
        self.label.place(x=0, y=0)

        self.line = LabelFrame(
            self.History,
            width=175,
            height=2,
            font=("Courier New", 15, "bold"),
            bg=self.bg,
            fg="white")
        self.line.place(x=0, y=25)

    def Draw_Basic(self):
        self.three = Button(
            self,
            text="3",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(3))
        self.three.place(x=570, y=250)

        self.two = Button(
            self,
            text="2",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(2))
        self.two.place(x=510, y=250)

        self.one = Button(
            self,
            text="1",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(1))
        self.one.place(x=450, y=250)

        self.six = Button(
            self,
            text="6",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(6))
        self.six.place(x=570, y=190)

        self.five = Button(
            self,
            text="5",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(5))
        self.five.place(x=510, y=190)

        self.four = Button(
            self,
            text="4",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(4))
        self.four.place(x=450, y=190)

        self.nine = Button(
            self,
            text="9",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(9))
        self.nine.place(x=570, y=130)

        self.eight = Button(
            self,
            text="8",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(8))
        self.eight.place(x=510, y=130)

        self.seven = Button(
            self,
            text="7",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(7))
        self.seven.place(x=450, y=130)

        self.factorial = Button(
            self,
            text="n!",
            bg="#414658",
            fg="white",
            font=("Courier New", 8, "bold"),
            pady=15,
            padx=15,
            command= self.func.factorial_score)
        self.factorial.place(x=320, y=130)

        self.sinus = Button(
            self,
            text="sin",
            bg="#414658",
            fg="white",
            font=("Courier New", 6, "bold"),
            pady=15,
            padx=15,
            command=self.func.sinus_score)
        self.sinus.place(x=320, y=190)

        self.cosinus = Button(
            self,
            text="cos",
            bg="#414658",
            fg="white",
            font=("Courier New", 6, "bold"),
            pady=15,
            padx=15,
            command=self.func.cosinus_score)
        self.cosinus.place(x=320, y=250)

        self.tan = Button(
            self,
            text="tg",
            bg="#414658",
            fg="white",
            font=("Courier New", 6, "bold"),
            pady=15,
            padx=15,
            command=self.func.tan_score)
        self.tan.place(x=320, y=310)

        self.ctg = Button(
            self,
            text="ctg",
            bg="#414658",
            fg="white",
            font=("Courier New", 6, "bold"),
            pady=15,
            padx=15,
            command=self.func.catan_score)
        self.ctg.place(x=320, y=370)

        self.stupin = Button(
            self,
            text="x^y",
            bg="#414658",
            fg="white",
            font=("Courier New", 8, "bold"),
            pady=15,
            padx=15,
            command=lambda: self.func.click_btn("^"))
        self.stupin.place(x=380, y=130)

        self.sqrt = Button(
            self,
            text="√",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("^0.5"))
        self.sqrt.place(x=380, y=190)

        self.procent = Button(
            self,
            text="%",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=self.func.procent_score)
        self.procent.place(x=380, y=250)

        self.log = Button(
            self,
            text="log",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.log_score)
        self.log.place(x=380, y=310)

        self.equal = Button(
            self,
            text="=",
            bg="#252832",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            height=1,
            command=lambda: [self.func.equal_btn(), self.add_to_history()]
        )
        self.equal.place(x=630, y=310)

        self.zero = Button(
            self,
            text="0",
            bg=self.bg,
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(0))
        self.zero.place(x=510, y=310)

        self.C = Button(
            self,
            text="C",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=self.func.clr_btn)
        self.C.place(x=450, y=70)

        self.Del = Button(
            self,
            text="Del",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=self.func.del_btn)
        self.Del.place(x=530, y=70)

        self.add = Button(
            self,
            text="+",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("+"))
        self.add.place(x=630, y=250)

        self.sub = Button(
            self,
            text="-",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("-"))
        self.sub.place(x=630, y=190)

        self.mul = Button(
            self,
            text="*",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("*"))
        self.mul.place(x=630, y=130)

        self.div = Button(
            self,
            text="/",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("/"))
        self.div.place(x=630, y=70)

        self.point = Button(
            self,
            text=".",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("."))
        self.point.place(x=570, y=310)

        self.negative = Button(
            self,
            text="-/+",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=5,
            command=lambda: self.func.click_btn("-"))
        self.negative.place(x=450, y=310)

        self.leftsc = Button(
            self,
            text="(",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn("("))
        self.leftsc.place(x=450, y=370)

        self.righttsc = Button(
            self,
            text=")",
            bg="#414658",
            fg="white",
            font=("Courier New", 12, "bold"),
            pady=10,
            padx=15,
            command=lambda: self.func.click_btn(")"))
        self.righttsc.place(x=510, y=370)

        self.ms = Button(
            self,
            text="MS",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.save_m)
        self.ms.place(x=570, y=370)

        self.mr = Button(
            self,
            text="MR",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.print_m)
        self.mr.place(x=630, y=370)

        self.mc = Button(
            self,
            text="MC",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.clear_m)
        self.mc.place(x=450, y=430)

        self.mplus = Button(
            self,
            text="M+",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.m_plus)
        self.mplus.place(x=510, y=430)

        self.mminus = Button(
            self,
            text="M-",
            bg="#414658",
            fg="white",
            font=("Courier New", 10, "bold"),
            pady=10,
            padx=15,
            command=self.func.m_minus)
        self.mminus.place(x=570, y=430)

    def add_to_history(self):
        global f
        self.Hist_num["text"] = self.claculation.get()
        f.write(str(self.claculation.get()) + '\n')


class functions():
    def __init__(self):
        super().__init__()

        self.operator = ''
        self.equation = StringVar()
        self.memory = ''

    def save_m(self):
        global operator
        self.memory = self.operator

    def sinus_score(self):
        global operator
        try:
            temp = math.sin(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print('Wrong use sinus')

    def cosinus_score(self):
        global operator
        try:
            temp = math.cos(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print('Wrong use cosinus')

    def tan_score(self):
        global operator
        try:
            temp = math.tan(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print('Wrong use tangense')

    def catan_score(self):
        global operator
        try:
            temp = math.cos(int(self.equation.get())) / math.sin(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print('Wrong use catangense')

    def factorial_score(self):
        global operator
        try:
            temp = math.factorial(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print('Wrong use factorial')

    def log_score(self):
        global operator
        try:
            temp = math.log10(int(self.equation.get()))
            self.equation.set(str(temp))
            self.operator = self.equation.get()
        except Exception:
            print("Wrong using log")

    def procent_score(self):
        global operator
        ready = ''
        temp = str(self.equation.get())
        digitals = ['-', '+', '/', '*', '^']
        for i in range(len(digitals)):
            if temp.find(digitals[i]) != -1:
                new = temp.split(digitals[i])
                refactor = str('{:f}'.format(int(new[0]) / 100 * int(new[1])))
                ready = str(new[0]) + str(digitals[i]) + str(refactor)
        self.equation.set(str(ready))
        self.operator = self.equation.get()
        print(temp)
        pass

    def print_m(self):
        global operator
        global memory
        self.operator = self.operator + str(self.memory)
        self.equation.set(self.operator)

    def clear_m(self):
        global memory
        self.memory = ''

    def m_plus(self):
        global operator
        global memory
        self.memory = str(int(self.memory)+int(self.equation.get()))

    def m_minus(self):
        global operator
        global memory
        self.memory = str(int(self.memory)-int(self.equation.get()))

    def click_btn(self, number):
        global operator
        self.operator = self.operator + str(number)
        self.equation.set(self.operator)

    def equal_btn(self):
        global operator
        temp = Expression(self.operator)
        global ans
        self.add = str(ans)
        self.equation.set(self.add)
        self.operator = ''

    def equal_btn(self):
        global operator
        temp = Expression(self.operator)
        global ans
        self.sub = str(ans)
        self.equation.set(self.sub)
        self.operator = ''

    def equal_btn(self):
        global operator
        temp = Expression(self.operator)
        global ans
        self.div = str(ans)
        self.equation.set(self.div)
        self.operator = ''

    def equal_btn(self):
        global operator
        temp = Expression(self.operator)
        global ans
        self.mult = str(ans)
        self.equation.set(self.mult)
        self.operator = ''

    def clr_btn(self):
        self.operator = ''
        self.equation.set('')

    def del_btn(self):
        self.operator = self.equation.get()[:-1]
        self.equation.set(self.equation.get()[:-1])


if __name__ == "__main__":
    app = Load()
    app.mainloop()
