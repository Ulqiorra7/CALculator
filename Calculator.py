from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import os
buttons = ['%','','C','<-','1/x','x^2',u'\u221a','/','7', '8', '9', '*','4', '5', '6', '-','1', '2', '3', '+', '+/-','0', '.', '=']
row_value, col_value, flag, text = 0, 0, '1', ''
Main_Form = Tk() 
Main_Form.geometry("250x300")
Main_Form.title("Калькулятор")
Main_Form.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + '\\favicon.ico')
label = ttk.Label(background="White",text="0",width="30",anchor='e')
label.pack(pady=2)
frame = tk.Frame(Main_Form)
frame.pack(pady=10)
def button_click(value):
    global flag, action, X, text
    if value in '0123456789.' and not(value=='.' and '.' in label.cget("text")):
        if (label.cget("text") == "0" or flag == '0') and value!='.': 
            flag = '1'
            label.config(text = value)  
        else: label.config(text = label.cget("text") + value)
    elif value == 'x^2' or value == '1/x' or value == '%' or value == u'\u221a' or value == '+/-':
        if value == 'x^2': text = str((float(label.cget("text")))**2)
        elif value == '%': text = str((float(label.cget("text")))/100)
        elif value == u'\u221a': text = str((float(label.cget("text")))**(0.5))
        elif value == '+/-': text = str((float(label.cget("text")))*(-1))
        else: 
            try: text = str(1/(float(label.cget("text")))) 
            except ZeroDivisionError: show_error_window("Ошибка: Деление на ноль!")
        if text[-2:] == '.0': text = text[:-2]
        label.config(text = text)
    elif value == '<-' and label.cget("text") != "0": label.config(text = label.cget("text")[:-1])
    else:
        if value in '+-/*':
            flag = '0' 
            action = value 
            X = float(label.cget("text"))
        elif value == 'C': 
            flag = '0'
            label.config(text = '0')
        elif value == '=' and flag == '1':
            if action == '+': text = str(X+float(label.cget("text")))
            elif action == '-': text = str(X-float(label.cget("text")))
            elif action == '/':
                try: text = str(X/float(label.cget("text")))
                except ZeroDivisionError: show_error_window("Ошибка: Деление на ноль!")
            elif action == '*': text = str(X*float(label.cget("text")))
            if text[-2:] == '.0': text = text[:-2]
            label.config(text = text)
    if label.cget("text") == "": label.config(text = "0")
def show_error_window(message):
    messagebox.showerror("Ошибка", message)

for button in buttons:
    btn = tk.Button(frame, text=button, width=5, height=2, command=lambda b=button: button_click(b))
    btn.grid(row=row_value, column=col_value)
    col_value += 1
    if col_value > 3:  
        col_value = 0
        row_value += 1
Main_Form.mainloop()

