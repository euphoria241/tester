# This Python file uses the following encoding: utf-8
from pysqlcipher3 import dbapi2 as sqlite3
from PyQt5.QtWidgets import (QWidget,QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QRadioButton, QLineEdit,qApp, QComboBox, QButtonGroup,QMessageBox)
from PyQt5.QtCore import QTimer
from TestTicket import TestTicket
from processController.process import CheckBox

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.processController = CheckBox()
        self.initUI()

    def initUI(self):
        # starting screen
        self.startButton = QPushButton("Начать тест")
        self.startButton.setDisabled(True)
        self.nameLine = QLineEdit()
        self.groupLine = QLineEdit()
        self.nameLine.setPlaceholderText("Введите свое имя и фамилию...")
        self.groupLine.setPlaceholderText("Введите группу...")
        self.nameLine.textChanged.connect(self.disableStartButton)
        self.groupLine.textChanged.connect(self.disableStartButton)
        self.get_tests()
        self.startButton.clicked.connect(self.start_button_handler)

        # test screen
        self.label = QLabel()
        self.radio1 = QRadioButton()
        self.radio2 = QRadioButton()
        self.radio3 = QRadioButton()
        self.radio4 = QRadioButton()
        self.asnwerField = QTextEdit()
        self.asnwerField.setFixedWidth(400)
        self.asnwerField.setFixedHeight(100)
        self.timeLeftTitle = QLabel("Оставшееся время: ")
        self.timeLeft = QLabel()
        self.radioGroup = QButtonGroup()
        self.answerButton = QPushButton("Ответить")
        self.skipButton = QPushButton("Пропустить")
        self.endButton = QPushButton("Завершить")
        self.answerButton.clicked.connect(self.answer_button_handler)
        self.skipButton.clicked.connect(self.skip_button_handel)
        self.endButton.clicked.connect(self.end_button_handler)
        
        # final screen
        self.resultLabel = QLabel()
        self.restartButton = QPushButton("На главный экран")
        self.restartButton.clicked.connect(self.restart_button_handler)

        #bottom layout with buttons
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.timeLeftTitle)
        self.bottomLayout.addWidget(self.timeLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.skipButton)
        self.bottomLayout.addWidget(self.answerButton)
        self.bottomLayout.addWidget(self.endButton)
        self.bottomLayout.addWidget(self.restartButton)

        # layout for test questions
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.questionsLayout= QVBoxLayout()
        self.radioGroup.addButton(self.radio1, 0)
        self.radioGroup.addButton(self.radio2, 1)
        self.radioGroup.addButton(self.radio3, 2)
        self.radioGroup.addButton(self.radio4, 3)
        
        self.questionsLayout.addWidget(self.label)
        self.questionsLayout.addWidget(self.radio1)
        self.questionsLayout.addWidget(self.radio2)
        self.questionsLayout.addWidget(self.radio3)
        self.questionsLayout.addWidget(self.radio4)
        self.questionsLayout.addWidget(self.nameLine)
        self.questionsLayout.addWidget(self.groupLine)
        self.nameLine.clearFocus()
        self.groupLine.clearFocus()
        self.questionsLayout.addWidget(self.asnwerField)
        self.questionsLayout.addWidget(self.testsComboBox)
        self.questionsLayout.addWidget(self.startButton)
        self.questionsLayout.addWidget(self.resultLabel)

        # main layout of widget
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.questionsLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.setContentsMargins(30,30,30,30)
        self.setLayout(self.mainLayout)
        
        self.label.hide()
        self.radio1.hide()
        self.radio2.hide()
        self.radio3.hide()
        self.radio4.hide()
        self.asnwerField.hide()
        self.answerButton.hide()
        self.skipButton.hide()
        self.endButton.hide()
        self.restartButton.hide()
        self.timeLeftTitle.hide()
        self.timeLeft.hide()
        self.resultLabel.hide()

    def disableStartButton(self):
        if len(self.nameLine.text()) > 0 and len(self.groupLine.text()) > 0:
            self.startButton.setDisabled(False)
        else:
            self.startButton.setDisabled(True)

    def on_timer(self):
        self.testTime -= 1
        if self.testTime % self.checkTimeout == 0:
            self.processController.check()
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
        connection = sqlite3.connect('file:database/encrypted_test.db?mode=rw', uri=True)
        cursor = connection.cursor()
        cursor.execute("PRAGMA key='DMEpython'")
        request = "select * from tests"
        cursor.execute(request)
        fetched_tests = cursor.fetchall()
        connection.close()

        self.testsComboBox = QComboBox()
        for test in fetched_tests:
            self.testsComboBox.addItem(str(test[0]) + " " + test[1] + " Семестр " + str(test[2]) + " Часть " + str(test[3]))

    def start_button_handler(self):
        self.processController.check()
        self.checkTimeout = 30
        self.ticket = TestTicket(self.testsComboBox.currentText().split(' ')[0],self.nameLine.text(),self.groupLine.text())
        self.nameLine.clear()
        self.nameLine.hide()
        self.groupLine.clear()
        self.groupLine.hide()
        self.testTime = self.ticket.get_test_time()
        self.startButton.hide()
        self.testsComboBox.hide()
        self.skipButton.show()
        self.endButton.show()
        self.answerButton.show()
        self.timeLeft.show()
        self.timeLeftTitle.show()
        self.timeLeft.setText(str(self.testTime // 60) + ":" + str(self.testTime % 60) + "0")
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
            self.asnwerField.show()
            qApp.processEvents()
            self.update()

        self.update()
        qApp.processEvents()

        # self.skip_button_handel()

    def answer_button_handler(self):
        if(self.radio1.isChecked() or self.radio2.isChecked() or self.radio3.isChecked() or self.radio4.isChecked() or (self.asnwerField.toPlainText() != '')):
            if (self.asnwerField.toPlainText() != ''):
                self.ticket.set_answer(self.asnwerField.toPlainText())
                print(self.asnwerField.toPlainText())
                print("LINE Written - ", self.asnwerField.toPlainText())
                self.asnwerField.clear()
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
        self.timer.stop()
        self.ticket.save_attempt()
        self.label.hide()
        self.resultLabel.show()
        self.restartButton.show()
        self.radio1.hide()
        self.radio2.hide()
        self.radio3.hide()
        self.radio4.hide()
        self.asnwerField.hide()
        self.asnwerField.clear()
        self.skipButton.hide()
        self.answerButton.hide()
        self.endButton.hide()
        self.timeLeftTitle.hide()
        self.timeLeft.hide()
        resultString = "Ваш результат "+ str(self.ticket.get_result())+" из " + str(len(self.ticket.questions)) + "!"
        self.resultLabel.setText(resultString)
        
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
            self.asnwerField.hide()
            #clear everything
            self.asnwerField.clear()
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
                self.asnwerField.show()
            qApp.processEvents()
            self.update()
        elif tempQuestion == -1:
            self.end_test()

    def restart_button_handler(self):
        self.resultLabel.hide()
        self.restartButton.hide()
        self.nameLine.show()
        self.groupLine.show()
        self.startButton.show()
        self.testsComboBox.show()
        qApp.processEvents()
        self.update()