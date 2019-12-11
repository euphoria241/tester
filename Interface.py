# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QRadioButton, QProgressBar, QLineEdit)
from PyQt5.QtCore import QTimer
from TestTicket import TestTicket


class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.ticket = TestTicket()
        self.initUI()

    def initUI(self):
        self.answerButton = QPushButton("Ответить")
        self.skipButton = QPushButton("Пропустить")
        self.endButton = QPushButton("Завершить")
        self.answerButton.clicked.connect(self.answer_button_handler)
        self.skipButton.clicked.connect(self.skip_button_handel)
        self.endButton.clicked.connect(self.end_button_handler)
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
        self.vbox.addLayout(self.qbox)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.label.hide()
        self.radio1.hide()
        self.radio2.hide()
        self.radio3.hide()
        self.radio4.hide()
        self.line.hide()

        # self.pb = QProgressBar()
        # self.pb.setMaximum(600)
        # self.pb.setMinimum(0)
        # self.pb.setValue(0)
        # self.qbox.addWidget(self.pb)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.on_timer)
        # self.timer.start(1000)

    # def on_timer(self):
    #     current_value = self.pb.value() + 1
    #     self.pb.setValue(current_value)
    #     if current_value == 600:
    #         self.timer.stop()
    def answer_button_handler(self):
        pass

    def end_button_handler(self):
        pass
        # self.label.setText("BBB234")
        # self.radio1.setText("fdf")
        # self.update()

    def skip_button_handel(self):
        tempQuestion = self.ticket.get_next_question_without_answer()
        if tempQuestion != -1:
            if len(tempQuestion.options) == 4:
                self.line.hide()
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

                self.label.show()
                self.radio1.show()
                self.radio2.show()
                self.radio3.show()
                self.radio4.show()

                self.update()
            elif len(tempQuestion.options) == 0:
                self.line.hide()
                self.radio1.hide()
                self.radio2.hide()
                self.radio3.hide()
                self.radio4.hide()
                self.line.hide()

                self.label.setText(tempQuestion.title)
                self.label.show()
                self.line.show()

                self.update()
    

    