# This Python file uses the following encoding: utf-8
import sys
import time
import sqlite3
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QRadioButton, QProgressBar, QLineEdit,qApp, QComboBox, QButtonGroup)
from PyQt5.QtCore import QTimer
from TestTicket import TestTicket


class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.startButton = QPushButton("Начать тест")
        self.answerButton = QPushButton("Ответить")
        self.skipButton = QPushButton("Пропустить")
        self.endButton = QPushButton("Завершить")

        self.get_tests()

        self.answerButton.clicked.connect(self.answer_button_handler)
        self.skipButton.clicked.connect(self.skip_button_handel)
        self.endButton.clicked.connect(self.end_button_handler)
        self.startButton.clicked.connect(self.start_button_handler)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.skipButton)
        self.hbox.addWidget(self.answerButton)
        self.hbox.addWidget(self.endButton)
        self.qbox= QVBoxLayout()
        self.label = QLabel()
        self.radio1 = QRadioButton()
        self.radio2 = QRadioButton()
        self.radio3 = QRadioButton()
        self.radio4 = QRadioButton()
        self.line = QLineEdit(self)
        self.vbox = QVBoxLayout()
        self.qbox.addWidget(self.label)
        self.qbox.addWidget(self.radio1)
        self.qbox.addWidget(self.radio2)
        self.qbox.addWidget(self.radio3)
        self.qbox.addWidget(self.radio4)
        self.qbox.addWidget(self.line)
        self.line.setFixedWidth(200)
        self.qbox.addWidget(self.testsComboBox)
        self.qbox.addWidget(self.startButton)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.qbox)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.vbox.setContentsMargins(30,30,30,30)
        self.setLayout(self.vbox)
        self.label.hide()
        self.radio1.hide()
        self.radio2.hide()
        self.radio3.hide()
        self.radio4.hide()
        self.line.hide()
        self.answerButton.hide()
        self.skipButton.hide()
        self.endButton.hide()

    def on_timer(self):
        current_value = self.pb.value() + 1
        self.pb.setValue(current_value)
        if current_value == 600:
            self.timer.stop()
            
    def get_tests(self):
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        request = "select * from tests"
        cursor.execute(request)
        fetched_tests = cursor.fetchall()
        connection.close()
        
        self.testsComboBox = QComboBox()
        for test in fetched_tests:
            self.testsComboBox.addItem(str(test[0]) + " " + test[1] + " Семестр " + str(test[2]) + " Часть " + str(test[3]))

    def hide_everything(self):
        pass

    def start_button_handler(self):
        self.ticket = TestTicket(self.testsComboBox.currentText())
        self.startButton.hide()
        self.testsComboBox.hide()
        self.skipButton.show()
        self.endButton.show()
        self.answerButton.show()
        # self.pb = QProgressBar()
        # self.pb.setMaximum(600)
        # self.pb.setMinimum(0)
        # self.pb.setValue(0)
        # self.qbox.addWidget(self.pb)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.on_timer)
        # self.timer.start(1000)6
        firstQuestion = self.ticket.get_current_question()
        if len(firstQuestion.options) == 4:
            self.label.setText(firstQuestion.title)
            self.radio1.setText(firstQuestion.options[0])
            self.radio2.setText(firstQuestion.options[1])
            self.radio3.setText(firstQuestion.options[2])
            self.radio4.setText(firstQuestion.options[3])
            self.label.show()
            self.radio1.show()
            self.radio2.show()
            self.radio3.show()
            self.radio4.show()
            qApp.processEvents()
            self.update()

        elif len(firstQuestion.options) == 0:
            self.label.setText(firstQuestion.title)
            self.label.show()
            self.line.show()
            qApp.processEvents()
            self.update()

        self.update()
        qApp.processEvents()
        # self.skip_button_handel()

    def answer_button_handler(self):
        if(self.radio1.isChecked() or self.radio2.isChecked() or self.radio3.isChecked() or self.radio4.isChecked() or (self.line.text != '')):
            if (self.line.text != ''):
                self.ticket.set_answer(self.line.text())
                print(self.line.text())
                print("LINE Written - ", self.line.text())
            elif(self.radio1.isChecked()):
                self.ticket.set_answer(self.radio1.text())
                print("BUT1 Written - ", self.radio1.text())
            elif(self.radio2.isChecked()):
                self.ticket.set_answer(self.radio2.text())
                
                print("BUT2 Written - ", self.radio2.text())
            elif(self.radio3.isChecked()):
                self.ticket.set_answer(self.radio3.text())
                print("BUT3 Written - ", self.radio3.text())
            else:
                self.ticket.set_answer(self.radio4.text())
                print("BUT4 Written - ", self.radio4.text())                
            self.skip_button_handel()
        else:
            print("No ANSWER!")

    def end_test(self):
        self.label.hide()
        self.radio1.hide()
        self.radio2.hide()
        self.radio3.hide()
        self.radio4.hide()
        self.line.hide()
        self.skipButton.hide()
        self.answerButton.hide()
        self.endButton.hide()
        # self.pb.hide()
        self.resultLabel = QLabel()
        resultString = "Your result is "+ str(self.ticket.get_result())+" of 10!"
        self.resultLabel.setText(resultString)
        self.qbox.addWidget(self.resultLabel)
        qApp.processEvents()
        self.update()

    def end_button_handler(self):
        self.end_test()

    def skip_button_handel(self):
        tempQuestion = self.ticket.get_next_question_without_answer()
        # print(tempQuestion.title)
        if tempQuestion != -1:
            if len(tempQuestion.options) == 4:
                self.label.hide()
                self.radio1.hide()
                self.radio2.hide()
                self.radio3.hide()
                self.radio4.hide()
                self.line.hide()
                self.label.setText(tempQuestion.title)

                self.radio1.setText(tempQuestion.options[0])
                self.radio2.setText(tempQuestion.options[1])
                self.radio3.setText(tempQuestion.options[2])
                self.radio4.setText(tempQuestion.options[3])
                print("Current result is - ", self.ticket.get_result())                
                self.label.show()
                self.radio1.show()
                self.radio2.show()
                self.radio3.show()
                self.radio4.show()

                qApp.processEvents()
                self.update()
            elif len(tempQuestion.options) == 0:
                self.label.hide()
                self.radio1.hide()
                self.radio2.hide()
                self.radio3.hide()
                self.radio4.hide()
                self.line.hide()
                self.label.setText(tempQuestion.title)
                self.label.show()
                self.line.show()
                print("Current result is - ", self.ticket.get_result())
                qApp.processEvents()

                self.update()
        elif tempQuestion == -1:
            self.end_test()