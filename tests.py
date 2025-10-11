import unittest
from unittest.mock import Mock

def button_click(value):
    global flag, action, X, text, label
    if value in '0123456789.' and not(value=='.' and '.' in label.cget("text")):
        if (label.cget("text") == "0" or flag == '0') and value!='.': 
            flag = '1'
            label.config(text = value)  
        else: label.config(text = label.cget("text") + value)
    elif value == 'x^2' or value == '1/x' or value == '%' or value == '\u221a' or value == '+/-':
        if value == 'x^2': text = str((float(label.cget("text")))**2)
        elif value == '%': text = str((float(label.cget("text")))/100)
        elif value == '\u221a': text = str((float(label.cget("text")))**(0.5))
        elif value == '+/-': text = str((float(label.cget("text")))*(-1))
        else: 
            try: text = str(1/(float(label.cget("text")))) 
            except ZeroDivisionError: pass
        if text and text[-2:] == '.0': text = text[:-2]
        label.config(text = text)
    elif value == '<-' and label.cget("text") != "0": 
        label.config(text = label.cget("text")[:-1])
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
            elif action == '/': text = str(X/float(label.cget("text")))
            elif action == '*': text = str(X*float(label.cget("text")))
            if text and text[-2:] == '.0': text = text[:-2]
            label.config(text = text)
    if label.cget("text") == "": label.config(text = "0")

class TestButtonClickSimple(unittest.TestCase):
    
    def setUp(self):
        global flag, action, X, text, label
        
        self.display_text = "0"
        
        def cget(prop):
            if prop == "text":
                return self.display_text
            return None
        
        def config(text=None):
            if text is not None:
                self.display_text = text
        
        self.label = Mock()
        self.label.cget = Mock(side_effect=cget)
        self.label.config = Mock(side_effect=config)
        
        label = self.label
        flag = '1'
        action = ''
        X = 0
        text = ''
    
    def test_1_simple_input(self):
        """Тест простого ввода цифр"""
        button_click("1")
        self.assertEqual(self.display_text, "1")
        
        button_click("2")
        self.assertEqual(self.display_text, "12")
        
        button_click("3")
        self.assertEqual(self.display_text, "123")
    
    def test_2_clear_operation(self):
        """Тест операции очистки"""
        button_click("5")
        self.assertEqual(self.display_text, "5")
        
        button_click("C")
        self.assertEqual(self.display_text, "0")
    
    def test_3_square_operation(self):
        """Тест возведения в квадрат"""
        button_click("4")
        button_click("x^2")
        self.assertEqual(self.display_text, "16")
    
    def test_4_square_root_operation(self):
        """Тест квадратного корня"""
        button_click("9")
        button_click("\u221a")
        self.assertEqual(self.display_text, "3")
    
    def test_5_sign_change(self):
        """Тест смены знака"""
        button_click("5")
        button_click("+/-")
        self.assertEqual(self.display_text, "-5")
        
        button_click("+/-") 
        self.assertEqual(self.display_text, "5")
    
    def test_6_addition(self):
        """Тест сложения: 5 + 3 = 8"""
        button_click("5")
        button_click("+")
        button_click("3")
        button_click("=")
        self.assertEqual(self.display_text, "8")
    
    def test_7_subtraction(self):
        """Тест вычитания: 10 - 4 = 6"""
        button_click("1")
        button_click("0")
        button_click("-")
        button_click("4")
        button_click("=")
        self.assertEqual(self.display_text, "6")
    
    def test_8_multiplication(self):
        """Тест умножения: 6 * 7 = 42"""
        button_click("6")
        button_click("*")
        button_click("7")
        button_click("=")
        self.assertEqual(self.display_text, "42")
    
    def test_9_division(self):
        """Тест деления: 15 / 3 = 5"""
        button_click("1")
        button_click("5")
        button_click("/")
        button_click("3")
        button_click("=")
        self.assertEqual(self.display_text, "5")
    
    def test_10_percentage(self):
        """Тест процентов"""
        button_click("5")
        button_click("0")
        button_click("%")
        self.assertEqual(self.display_text, "0.5")
    
    def test_11_reciprocal(self):
        """Тест обратного числа"""
        button_click("4")
        button_click("1/x")
        self.assertEqual(self.display_text, "0.25")
    
    def test_12_decimal_points(self):
        """Тест десятичных точек"""
        button_click("3")
        button_click(".")
        button_click("1")
        button_click("4")
        self.assertEqual(self.display_text, "3.14")
    
    def test_13_backspace(self):
        """Тест backspace"""
        button_click("1")
        button_click("2")
        button_click("3")
        button_click("<-")
        self.assertEqual(self.display_text, "12")
        button_click("<-")
        self.assertEqual(self.display_text, "1")
        button_click("<-")
        self.assertEqual(self.display_text, "0")
    
    def test_14_double_decimal_prevention(self):
        """Тест предотвращения двойной точки"""
        button_click("1")
        button_click(".")
        button_click(".")
        button_click("5")
        self.assertEqual(self.display_text, "1.5")
    
    def test_15_division_by_zero_prevention(self):
        """Тест обработки деления на ноль"""
        button_click("0")
        button_click("1/x")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
