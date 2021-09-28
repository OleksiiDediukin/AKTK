from tkinter import *
from tkinter import messagebox

class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.root = root
        self.width = 900
        self.height = 550
        self.formula = None
        self.entry = None
        self.entry_from = None
        self.entry_to = None
        self.count_btn = None
        self.fr = IntVar()
        self.fr.set(2)
        self.to = IntVar()
        self.to.set(10)
        self.result = ""
        self.accuracy = 5
        self.alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.build()

    def to_decimal_int(self, num, fr):
        if num[0] == "-":
            n = num[1:]
        else:
            n = num
        result = 0
        for i in range(len(n)):
            result += self.alpha.index(n[i]) * int(fr) ** (len(n)-i-1)

        return result if num[0] != "-" else -result

    def to_decimal_frac(self, num, fr):
        result = 0
        for i in range(len(num)):
            result += self.alpha.index(num[i]) * int(fr) ** (-i - 1)
        return result

    def from_int_decimal_to(self, num, to) -> str:
        result = ""
        while num >= to:
            result += self.alpha[num % to]
            num //= to
        if num > 0:
            result += self.alpha[num]
        return result[::-1]

    def from_frac_decimal_to(self, num: int, to: int) -> str:
        result = ""
        count = 0
        while num != int(num) and count < self.accuracy:
            result += self.alpha[int(num * to)]
            num = num * to - int((num * to))
            count += 1
        return result

    def to_decimal(self, expression, fr):
        integer_part = 0
        fractional_part = 0
        if "." in expression:
            integer_part, fractional_part = expression.split(".")
            return self.to_decimal_int(integer_part, fr), self.to_decimal_frac(fractional_part, fr)
        else:
            integer_part = expression
            return self.to_decimal_int(integer_part, fr), 0

    def to_notation(self, decimal_int, decimal_frac, to):
        int_to = self.from_int_decimal_to(decimal_int, to)
        frac_to = self.from_frac_decimal_to(decimal_frac, to)
        return int_to, frac_to


    def transfer(self):
        fr = self.fr.get()
        to = self.to.get()
        if fr == 666:
            try:
                fr = int(self.entry_from.get())
                if fr < 2 or fr > 36:
                    messagebox.showinfo(title="FROM field", message="Диапазон возможных значений: [2 .. 36]")
            except TypeError:
                raise TypeError("Field FROM must be not empty")
        if to == 666:
            try:
                to = int(self.entry_to.get())
                if to < 2 or to > 36:
                    messagebox.showinfo(title="TO field", message="Диапазон возможных значений: [2 .. 36]")
            except TypeError:
                raise TypeError("Field TO must be not empty")

        expression = self.entry.get()
        if expression[0] == "-":
            expression = expression[1:]
        int_part, frac_part = self.to_decimal(expression, fr)
        int_res, frac_res = self.to_notation(int_part, frac_part, to)
        if self.entry.get()[0] == "-":
            int_res = "-" + int_res
        if frac_res == "":
            self.result["text"] = int_res
        else:
            self.result["text"] = int_res + "." + frac_res

        self.root.update()

    def build(self):
        self.root.geometry(f"{self.width}x{self.height}+200+200")
        self.root.title("Калькулятор")
        self.root.resizable(False, False)
        self.formula = "0"
        Label(text="Введите выражение: ", foreground="#000", font=("Times New Roman", 11)).place(relx=0.01, rely=0.025)
        self.entry = Entry(bd=3, font=("Times New Roman", 14))
        self.entry.place(relx=0.16, rely=0.025, relheight=0.05, relwidth=0.8)
        self.entry.insert(0, "101")

        from_radiobutton = Radiobutton(text="Двоичная", value=2, variable=self.fr, padx=15, pady=10)
        from_radiobutton.place(relx=0.3, rely=0.2)
        from_radiobutton.select()
        Radiobutton(text="Троичная", value=3, variable=self.fr, padx=15, pady=10).place(relx=0.3, rely=0.25)
        Radiobutton(text="Восьмиричная", value=8, variable=self.fr, padx=15, pady=10).place(relx=0.3, rely=0.30)
        Radiobutton(text="Десятичная", value=10, variable=self.fr, padx=15, pady=10).place(relx=0.3, rely=0.35)
        Radiobutton(text="Шестнадцатиричная", value=16, variable=self.fr, padx=15, pady=10).place(relx=0.3, rely=0.40)
        Radiobutton(text="Другая", value=666, variable=self.fr, padx=15, pady=10).place(relx=0.3, rely=0.45)
        self.entry_from = Entry(bd=3, font=("Times New Roman", 14))
        self.entry_from.place(relx=0.4, rely=0.465, relheight=0.05, relwidth=0.08)

        Radiobutton(text="Двоичная", value=2, variable=self.to, padx=15, pady=10).place(relx=0.55, rely=0.2)
        Radiobutton(text="Троичная", value=3, variable=self.to, padx=15, pady=10).place(relx=0.55, rely=0.25)
        Radiobutton(text="Восьмиричная", value=8, variable=self.to, padx=15, pady=10).place(relx=0.55, rely=0.30)
        to_radiobutton = Radiobutton(text="Десятичная", value=10, variable=self.to, padx=15, pady=10)
        to_radiobutton.place(relx=0.55, rely=0.35)
        to_radiobutton.select()
        Radiobutton(text="Шестнадцатиричная", value=16, variable=self.to, padx=15, pady=10).place(relx=0.55, rely=0.40)
        Radiobutton(text="Другая", value=666, variable=self.to, padx=15, pady=10).place(relx=0.55, rely=0.45)
        self.entry_to = Entry(bd=3, font=("Times New Roman", 14))
        self.entry_to.place(relx=0.65, rely=0.465, relheight=0.05, relwidth=0.08)
        self.count_btn = Button(text="Перевести",
                                font=("Times New Roman", 15),
                                command=self.transfer)
        self.count_btn.place(relx=0.45, rely=0.55, width=150, height=20)

        Label(text="Результат", foreground="#000", font=("Times New Roman", 18)).place(relx=0.48, rely=0.65)
        self.result = Label(text="", foreground="#000", font=("Times New Roman", 15))
        self.result.place(relx=0.48, rely=0.75)


if __name__ == '__main__':
    root = Tk()
    app = Main(root)
    app.pack()
    root.mainloop()
