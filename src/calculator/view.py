import sys
import os
import re
from PySide2 import QtWidgets, QtCore, QtGui
import client

DIVIDE_CHAR = chr(247)
MULTIPLY_CHAR = chr(215)
PERCENT_PATTERN = re.compile(r'(\d*\.?\d*\%)')


class CalculatorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CalculatorWindow, self).__init__(parent=parent)

        self.client = client.Client()
        self.expression = ''

        self.field = QtWidgets.QLineEdit()
        self.field.setReadOnly(True)
        self.field.setAlignment(QtCore.Qt.AlignRight)

        self.divide_btn = QtWidgets.QPushButton(DIVIDE_CHAR)
        self.multiply_btn = QtWidgets.QPushButton(MULTIPLY_CHAR)
        self.subtract_btn = QtWidgets.QPushButton('-')
        self.plus_btn = QtWidgets.QPushButton('+')
        self.equal_btn = QtWidgets.QPushButton('=')
        self.zero_btn = QtWidgets.QPushButton('0')
        self.one_btn = QtWidgets.QPushButton('1')
        self.two_btn = QtWidgets.QPushButton('2')
        self.three_btn = QtWidgets.QPushButton('3')
        self.four_btn = QtWidgets.QPushButton('4')
        self.five_btn = QtWidgets.QPushButton('5')
        self.six_btn = QtWidgets.QPushButton('6')
        self.seven_btn = QtWidgets.QPushButton('7')
        self.eight_btn = QtWidgets.QPushButton('8')
        self.nine_btn = QtWidgets.QPushButton('9')
        self.decimal_btn = QtWidgets.QPushButton('.')
        self.del_btn = QtWidgets.QPushButton('DEL')
        self.clear_btn = QtWidgets.QPushButton('C')
        self.parenthesis_btn = QtWidgets.QPushButton('( )')
        self.percent_btn = QtWidgets.QPushButton('%')

        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QGridLayout(content_widget)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(QtCore.Qt.AlignTop)

        # Row 1
        content_layout.addWidget(self.field, 0, 0, 2, 4)

        # Row 2
        content_layout.addWidget(self.clear_btn, 2, 0, 1, 1)
        content_layout.addWidget(self.parenthesis_btn, 2, 1, 1, 1)
        content_layout.addWidget(self.percent_btn, 2, 2, 1, 1)
        content_layout.addWidget(self.divide_btn, 2, 3, 1, 1)

        # Row 3
        content_layout.addWidget(self.seven_btn, 3, 0, 1, 1)
        content_layout.addWidget(self.eight_btn, 3, 1, 1, 1)
        content_layout.addWidget(self.nine_btn, 3, 2, 1, 1)
        content_layout.addWidget(self.multiply_btn, 3, 3, 1, 1)

        # Row 4
        content_layout.addWidget(self.four_btn, 4, 0, 1, 1)
        content_layout.addWidget(self.five_btn, 4, 1, 1, 1)
        content_layout.addWidget(self.six_btn, 4, 2, 1, 1)
        content_layout.addWidget(self.subtract_btn, 4, 3, 1, 1)

        # Row 5
        content_layout.addWidget(self.one_btn, 5, 0, 1, 1)
        content_layout.addWidget(self.two_btn, 5, 1, 1, 1)
        content_layout.addWidget(self.three_btn, 5, 2, 1, 1)
        content_layout.addWidget(self.plus_btn, 5, 3, 1, 1)

        # Row 6
        content_layout.addWidget(self.zero_btn, 6, 0, 1, 1)
        content_layout.addWidget(self.decimal_btn, 6, 1, 1, 1)
        content_layout.addWidget(self.del_btn, 6, 2, 1, 1)
        content_layout.addWidget(self.equal_btn, 6, 3, 1, 1)

        self.setWindowTitle('Network Calculator')
        self.setCentralWidget(content_widget)

        self.divide_btn.clicked.connect(lambda x: self.add_operator(DIVIDE_CHAR))
        self.multiply_btn.clicked.connect(lambda x: self.add_operator(MULTIPLY_CHAR))
        self.subtract_btn.clicked.connect(lambda x: self.add_operator('-'))
        self.plus_btn.clicked.connect(lambda x: self.add_operator('+'))
        self.equal_btn.clicked.connect(self.submit_expression)
        self.zero_btn.clicked.connect(lambda x: self.add_number('0'))
        self.one_btn.clicked.connect(lambda x: self.add_number('1'))
        self.two_btn.clicked.connect(lambda x: self.add_number('2'))
        self.three_btn.clicked.connect(lambda x: self.add_number('3'))
        self.four_btn.clicked.connect(lambda x: self.add_number('4'))
        self.five_btn.clicked.connect(lambda x: self.add_number('5'))
        self.six_btn.clicked.connect(lambda x: self.add_number('6'))
        self.seven_btn.clicked.connect(lambda x: self.add_number('7'))
        self.eight_btn.clicked.connect(lambda x: self.add_number('8'))
        self.nine_btn.clicked.connect(lambda x: self.add_number('9'))
        self.decimal_btn.clicked.connect(lambda x: self.add_number('.'))
        self.del_btn.clicked.connect(self.delete_character)
        self.clear_btn.clicked.connect(self.clear_all)
        self.parenthesis_btn.clicked.connect(self.add_parenthesis)
        self.percent_btn.clicked.connect(lambda x: self.add_number('%'))

        stylesheet_file = os.path.join(os.path.dirname(__file__), 'resources', 'style.css')
        with open(stylesheet_file, 'r') as fp:
            self.setStyleSheet(fp.read())

    # def sizeHint(self):
    #     return QtCore.QSize(350, 622)

    def add_number(self, v):
        if self.expression:
            last_char = self.expression[-1]
            if v == '.':
                if not last_char.isnumeric():
                    self.expression += '0' + v
                else:
                    self.expression += v
            elif v == '.':
                return
            else:
                self.expression += v
        else:
            self.expression += v

        self.field.setText(self.expression)

    def add_operator(self, v):
        if not self.expression:
            # Only subtract op can be added to an empty expression for signs.
            if v == '-':
                self.expression += v
            else:
                return
        else:
            # If the last character is another operator, swap it.
            last_char = self.expression[-1]
            if last_char in (MULTIPLY_CHAR, DIVIDE_CHAR, '+', '-'):
                if v == '-' and last_char in (MULTIPLY_CHAR, DIVIDE_CHAR):
                    self.expression += v
                else:
                    self.expression = self.expression[:-1] + v
            else:
                self.expression += v

        self.field.setText(self.expression)

    def delete_character(self):
        self.expression = self.expression[:-1]
        self.field.setText(self.expression)

    def clear_all(self):
        self.expression = ''
        self.field.setText('')

    def add_parenthesis(self):
        char = '('

        start_count = self.expression.count('(')
        end_count = self.expression.count(')')

        if self.expression:
            if self.expression[-1].isnumeric():
                if start_count > end_count:
                    char = ')'
            elif self.expression[-1] == ')' and start_count > end_count:
                char = ')'

        self.expression += char

        self.field.setText(self.expression)

    def submit_expression(self):
        def _replace_percent(obj):
            print(obj.group(0))
            return str(float(obj.group(0)[:-1]) / 100)

        e = self.expression
        e = PERCENT_PATTERN.sub(_replace_percent, e)
        e = e.replace(MULTIPLY_CHAR, '*')
        e = e.replace(DIVIDE_CHAR, '/')
        print(e)
        #self.client.run(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    app.exec_()