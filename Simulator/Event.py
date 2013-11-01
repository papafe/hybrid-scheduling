
class Event(object):
    
    def __init__(self,timestamp,taskInstance,eventType):
        self.taskInstance = taskInstance
        self.eventType = eventType
        self.timestamp = timestamp        
    
    def __str__(self):
        
        var = [str(el) for el in [self.timestamp,self.taskInstance,self.eventType]]
        s = "("+",".join(var) + ")"
        return s
        
    def __repr__(self):
        return self.__str__()

                
        