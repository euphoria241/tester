import random
from pysqlcipher3 import dbapi2 as sqlite3
from datetime import datetime
from Question import Question

class TestTicket:

    def __init__(self, testId:int, studentName:str, studentGroup:str):
        self.questions = []
        self.topicId = testId
        self.generate_questions()
        self.studentName = studentName
        self.studentGroup = studentGroup
    
    def generate_questions(self):
        connection = sqlite3.connect('file:database/encrypted_test.db?mode=rw', uri=True)
        cursor = connection.cursor()
        cursor.execute("PRAGMA key='DMEpython'")
        request = "select * from questions where test_id =?"
        cursor.execute(request, (self.topicId,))
        fetched_questions = cursor.fetchall()
        if len(fetched_questions) > 9:
            questionsList = random.sample(fetched_questions, k=10)
        else:
            questionsList = random.sample(fetched_questions, k=len(fetched_questions))

        numerator = 1
        for question in questionsList:
            if question[2] != None:
                obj = Question(str(numerator) + ". " +  question[1], question[2].split(", "), question[3])
                self.questions.append(obj)
            else:
                obj = Question(str(numerator) + ". " + question[1], [], question[3])
                self.questions.append(obj)
            numerator += 1
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

    def get_test_time(self):
        connection = sqlite3.connect('file:database/encrypted_test.db?mode=rw', uri=True)
        cursor = connection.cursor()
        cursor.execute("PRAGMA key='DMEpython'")
        request = "select time from tests where test_id =?"
        cursor.execute(request, (self.topicId,))
        fetched_time = cursor.fetchone()
        connection.close()
        return fetched_time[0]


    def set_answer(self, answer):
        self.questions[self.currentQuestion].actualAnswer = answer
        self.questionsLeft -= 1

    def get_current_question(self):
        return self.questions[self.currentQuestion]

    def get_next_question_without_answer(self):
        index = self.find_next_question()
        if index != -1:
            return self.questions[index]
        else:
            return -1

    def get_result(self):
        result = 0
        for question in self.questions:
            if question.actualAnswer == question.rightAnswer:
                result += 1
        return result
    def save_attempt(self):
        connection = sqlite3.connect('file:database/encrypted_test.db?mode=rw', uri=True)
        cursor = connection.cursor()
        cursor.execute("PRAGMA key='DMEpython'")
        insert_query = "INSERT INTO attempts(student_name,student_group,score,date,test_id) VALUES(?,?,?,?,?)"
        dataTuple = (self.studentName,self.studentGroup,self.get_result(),datetime.now().strftime("%d/%m/%Y %H:%M:%S"),self.topicId)
        cursor.execute(insert_query, dataTuple)
        connection.commit()
        cursor.close()
        connection.close()