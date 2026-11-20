import tkinter as tk
from tkinter import font

def evaluate(expr: str) -> str:
    try:
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expr):
            return "Error"
        result = eval(expr, {"__builtins__": {}}, {})
        return str(int(result) if isinstance(result, float) and result.is_integer() else result)
    except ZeroDivisionError:
        return "Error: ÷ by 0"
    except Exception:
        return "Error"

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.expr = ""

        # Display
        self.display_font = font.Font(family="Segoe UI", size=28)
        self.display = tk.Entry(
            root, font=self.display_font, justify="right", bd=0,
            highlightthickness=2, highlightbackground="#ccc",
            highlightcolor="#0066cc", insertwidth=2
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=12, pady=12, ipady=10, sticky="ew")
        self.display.insert(0, "0")

        # Button layout
        buttons = [
            ("C", 1, 0, 2, "func"), ("⌫", 1, 2, 1, "func"), ("%", 1, 3, 1, "func"),
            ("7", 2, 0, 1, "num"), ("8", 2, 1, 1, "num"), ("9", 2, 2, 1, "num"), ("÷", 2, 3, 1, "op"),
            ("4", 3, 0, 1, "num"), ("5", 3, 1, 1, "num"), ("6", 3, 2, 1, "num"), ("×", 3, 3, 1, "op"),
            ("1", 4, 0, 1, "num"), ("2", 4, 1, 1, "num"), ("3", 4, 2, 1, "num"), ("−", 4, 3, 1, "op"),
            ("0", 5, 0, 2, "num"), (".", 5, 2, 1, "num"), ("+", 5, 3, 1, "op"),
            ("=", 6, 0, 4, "eq"),
        ]

        colors = {
            "num": ("#fff", "#1e1e1e", "#f0f0f0"),
            "op": ("#0066cc", "#fff", "#0052a3"),
            "func": ("#f0f0f0", "#333", "#e0e0e0"),
            "eq": ("#28a745", "#fff", "#218838"),
        }

        btn_font = font.Font(family="Segoe UI", size=14, weight="bold")

        for (text, r, c, span, kind) in buttons:
            bg, fg, active = colors[kind]
            btn = tk.Button(
                root, text=text, font=btn_font, bg=bg, fg=fg,
                activebackground=active, activeforeground=fg,
                bd=0, command=lambda t=text, k=kind: self.on_click(t, k)
            )
            btn.grid(row=r, column=c, columnspan=span, padx=6, pady=6, ipadx=10, ipady=10, sticky="nsew")

        # Keyboard support
        root.bind("<Key>", self.on_key)
        root.bind("<Return>", lambda e: self.on_click("=", "eq"))
        root.bind("<KP_Enter>", lambda e: self.on_click("=", "eq"))
        root.bind("<Escape>", lambda e: self.on_click("C", "func"))
        root.bind("<BackSpace>", lambda e: self.on_click("⌫", "func"))

        for i in range(4):
            root.columnconfigure(i, weight=1)
        for i in range(7):
            root.rowconfigure(i, weight=1)

    def on_click(self, text, kind):
        if kind == "num":
            if text == "." and "." in self.expr.split("+")[-1].split("-")[-1].split("*")[-1].split("/")[-1]:
                return
            self.expr += text
            self.update_display()
        elif kind == "op":
            if self.expr and self.expr[-1] in "+-*/":
                self.expr = self.expr[:-1]
            self.expr += {"÷": "/", "×": "*", "−": "-"}.get(text, text)
            self.update_display()
        elif kind == "func":
            if text == "C":
                self.expr = ""
            elif text == "⌫":
                self.expr = self.expr[:-1]
            elif text == "%":
                self.expr += "*0.01"
            self.update_display()
        elif kind == "eq":
            self.expr = evaluate(self.expr)
            self.update_display()

    def on_key(self, e):
        key = e.char
        if key.isdigit() or key in "+-*/.":
            self.on_click(key, "num" if key.isdigit() or key == "." else "op")
        elif key == "%":
            self.on_click("%", "func")

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr or "0")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()