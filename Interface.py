# This Python file uses the following encoding: utf-8
import sys
import time
import sqlite3
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QRadioButton, QProgressBar, QLineEdit,qApp, QComboBox, QButtonGroup,QMessageBox)
from PyQt5.QtCore import QTimer
from TestTicket import TestTicket

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.startButton = QPushButton("Начать тест")
        self.get_tests()
        self.startButton.clicked.connect(self.start_button_handler)

        self.answerButton = QPushButton("Ответить")
        self.skipButton = QPushButton("Пропустить")
        self.endButton = QPushButton("Завершить")
        self.answerButton.clicked.connect(self.answer_button_handler)
        self.skipButton.clicked.connect(self.skip_button_handel)
        self.endButton.clicked.connect(self.end_button_handler)

        self.hbox = QHBoxLayout()
        self.timeLeftTitle = QLabel("Оставшееся время: ")
        self.timeLeft = QLabel()
        self.hbox.addWidget(self.timeLeftTitle)
        self.hbox.addWidget(self.timeLeft)
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
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.radio1, 0)
        self.radioGroup.addButton(self.radio2, 1)
        self.radioGroup.addButton(self.radio3, 2)
        self.radioGroup.addButton(self.radio4, 3)
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
        self.timeLeftTitle.hide()
        self.timeLeft.hide()

    def on_timer(self):
        self.testTime -= 1
        minutes = self.testTime // 60
        seconds = self.testTime % 60
        if len(str(seconds)) != 1:
            self.timeLeft.setText(str(minutes) + ":" + str(seconds))
        else:
            self.timeLeft.setText(str(minutes) + ":0" + str(seconds))
        if self.testTime <= 0:
            self.timer.stop()
            self.end_test()

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
        self.ticket = TestTicket(self.testsComboBox.currentText().split(' ')[0])
        self.testTime = self.ticket.get_test_time()
        self.startButton.hide()
        self.testsComboBox.hide()
        self.skipButton.show()
        self.endButton.show()
        self.answerButton.show()
        self.timeLeft.show()
        self.timeLeftTitle.show()
        self.timeLeft.setText(str(self.testTime // 60) + ":" + str(self.testTime % 60) + "0")
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000)
        qApp.processEvents()
        self.update()
        
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
        if(self.radio1.isChecked() or self.radio2.isChecked() or self.radio3.isChecked() or self.radio4.isChecked() or (self.line.text() != '')):
            if (self.line.text() != ''):
                self.ticket.set_answer(self.line.text())
                print(self.line.text())
                print("LINE Written - ", self.line.text())
                self.line.clear()
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Ошибка")
            msg.setText("Выберибе или введите вариант ответа!")
            msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()

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
        self.timeLeftTitle.hide()
        self.timeLeft.hide()
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
        #check if there are any questions left
        if tempQuestion != -1:
            #hide everything
            self.label.hide()
            self.radio1.hide()
            self.radio2.hide()
            self.radio3.hide()
            self.radio4.hide()
            self.line.hide()
            #clear everything
            self.line.clear()
            self.radioGroup.setExclusive(False)
            self.radio1.setChecked(False)
            self.radio2.setChecked(False)
            self.radio3.setChecked(False)
            self.radio4.setChecked(False)
            self.radioGroup.setExclusive(True) 
            #print current result
            print("Current result is - ", self.ticket.get_result())  
            #fill form with new question
            if len(tempQuestion.options) == 4:
                self.label.setText(tempQuestion.title)
                self.radio1.setText(tempQuestion.options[0])
                self.radio2.setText(tempQuestion.options[1])
                self.radio3.setText(tempQuestion.options[2])
                self.radio4.setText(tempQuestion.options[3])
              
                self.label.show()
                self.radio1.show()
                self.radio2.show()
                self.radio3.show()
                self.radio4.show()
            elif len(tempQuestion.options) == 0:
                self.label.setText(tempQuestion.title)
                self.label.show()
                self.line.show()
            qApp.processEvents()
            self.update()
        elif tempQuestion == -1:
            self.end_test()