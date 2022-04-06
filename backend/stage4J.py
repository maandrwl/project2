import os

class judge:

        def __init__(self, fStage4):
                self.fStage4 = fStage4
                self.PATH_OUTPUT = fStage4['PATH_OUTPUT']
                self.path_assignment = fStage4['path_assignment']
                self.score = 0
                self.total = {'result':{}}
        
        def judgeFormat(self):
                try:
                        output_file = os.listdir(self.path_assignment)
                        for name_file in output_file:
                                file_out = open(os.path.join(self.PATH_OUTPUT, name_file), "r")
                                file_answer = open(os.path.join(self.path_assignment, name_file), "r")
                                file_out = file_out.read()
                                file_answer = file_answer.read()
                                if(file_out == file_answer):
                                        tranfer = {"status":"correct"}
                                        self.total['result'].update({name_file:tranfer})
                                        self.score = self.score + 1
                                else:
                                        tranfer = {
                                        "status": "Not correct!!",
                                        "output": file_out,
                                        "answer": file_answer
                                        }
                                        self.total['result'].update({name_file:tranfer})
                                os.remove(os.path.join(self.PATH_OUTPUT, name_file))
                        self.score = (self.score/len(output_file))*100
                        self.total['totalScore'] = self.score
                        self.total['queueFolder'] = {
                        'PATH_OUTPUT': self.PATH_OUTPUT,
                        'queueFolder': self.fStage4['queueFolder']
                        }
                except FileNotFoundError as e:
                        print(e)


        def judgeUnFormat(self):
                output_file = os.listdir(self.path_assignment)
                for name_file in output_file:
                        file_out = open(os.path.join(self.PATH_OUTPUT, name_file), "r")
                        file_answer = open(os.path.join(self.path_assignment, name_file), "r")
                        file_out = file_out.read()
                        file_out = file_out.replace('\n', '')
                        file_answer = file_answer.read()
                        file_answer = file_answer.replace('\n', '')
                        if(file_out == file_answer):
                                tranfer = {"status":"correct"}
                                self.total['result'].update({name_file:tranfer})
                                self.score = self.score + 1
                        else:
                                tranfer = {
                                "status": "Not correct!!",
                                "output": file_out,
                                "answer": file_answer
                                }
                                self.total['result'].update({name_file:tranfer})
                        os.remove(os.path.join(self.PATH_OUTPUT, name_file))
                self.score = (self.score/len(output_file))*100
                self.total['totalScore'] = self.score
                self.total['queueFolder'] = {
                        'PATH_OUTPUT': self.PATH_OUTPUT,
                        'queueFolder': self.fStage4['queueFolder']
                        }

        def getScore(self):
                return self.total