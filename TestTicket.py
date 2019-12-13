import json
import random
import sqlite3
from Question import Question

class TestTicket:

    def __init__(self):
        self.questions = []
        self.generate_questions()
    
    def generate_questions(self):
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        request = "select * from questions"
        cursor.execute(request)
        fetched_questions = cursor.fetchall()
        questionsList = random.sample(fetched_questions, k=12)

        for question in questionsList:
            if len(question[2]):
                obj = Question(question[1], question[2].split(", "), question[3])
                self.questions.append(obj)
            else:
                obj = Question(question[1], [], question[3])
                self.questions.append(obj)

        self.currentQuestion = 0
        self.nextQuestion = 1
        self.questionsLeft = len(self.questions)
        connection.close()
        
    def find_next_question(self):
        if self.questionsLeft != 0:
            while(self.questions[self.nextQuestion].actualAnswer != ''):
                if self.nextQuestion == (len(self.questions) - 1):
                    self.nextQuestion = 0
                else:
                    self.nextQuestion += 1

            self.currentQuestion = self.nextQuestion

            if self.nextQuestion == (len(self.questions)- 1):
                self.nextQuestion = 0
            else:
                self.nextQuestion += 1
            return self.currentQuestion
        else:
            return -1

    def set_answer(self, answer):
        self.questions[self.currentQuestion].actualAnswer = answer
        self.questionsLeft -= 1
        self.find_next_question()

    def get_current_question(self):
        return self.questions[self.currentQuestion]

    def get_next_question_without_answer(self):
        index = self.find_next_question()
        if index != -1:
            return self.questions[index]
        else:
            return -1