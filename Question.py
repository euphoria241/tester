class Question:
    def __init__(self, title:str, options, rightAnswer:str):
        self.title = title
        self.options = options.copy()
        self.rightAnswer = rightAnswer
        self.actualAnswer = ''