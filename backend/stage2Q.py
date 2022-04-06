from queue import Queue
class manageQ:
    q = Queue(maxsize = 100) 
    pQueue = 1
    cQueue = 0

    def qEmpty(self):
        return self.q.empty()

    def setcQueue(self):
        self.cQueue = self.cQueue + 1
        return self.cQueue
    
    def setpQueue(self):
        self.pQueue = self.pQueue + 1

    def checkQ(self, cQ):
        if self.pQueue == cQ:
            return True
        else: return False

    def getpQueue(self):
        return self.pQueue
    
    def getcQueue(self):
        return self.cQueue

    def putQ(self, inputQueue):
        self.q.put(inputQueue)

    def sentQueue(self):
        sent = self.q.get()
        return sent

    def getAPI(self, language):
        if (language == 'java'):
            return '/stage3J'
        elif (language == 'py'):
            return '/stage3P'

