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
Main_Form.iconbitmap(os.path.dirname(os.path.realpath(file)) + '\\favicon.ico')
label = ttk.Label(background="White",text="0",width="30",anchor='e')
label.pack(pady=2)
frame = tk.Frame(Main_Form)
frame.pack(pady=10)
#def button_click(value):

#for button in buttons:
#    btn = tk.Button(frame, text=button, width=5, height=2, command=lambda b=button: button_click(b))
#    btn.grid(row=row_value, column=col_value)
#    col_value += 1
#    if col_value > 3:  
#        col_value = 0
#        row_value += 1
Main_Form.mainloop()
