

def produce(self, unitTime):
    if self.queue[0] >= unitTime:
        Queue = self.queue
        newqueue = [0,0,0,0,0]
        newflag = [0,0,0,0,0]
        for slot in Queue:
            num = Queue.index(slot) + 1
            newqueue[Queue.index(slot)] = Queue[num]
        Queue = newqueue
        for slot in self.proflag:
            num = self.proflag.index(slot) + 1
            newflag[self.proflag.index(slot)] = self.proflag[num]
        self.proflag = newflag
        Queue[4] = 0
        self.queue = newqueue
        return True