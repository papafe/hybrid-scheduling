from EventType import EventType
from Event import Event
from EventList import EventList
from Instance import Instance
from Task import Task
from PriorityQueue import PriorityQueue

class Scheduler(object):
    """
    The scheduler executes tasks instance in the simulator.
    Attributes :
        active      The active task on the scheduler
        waiting     A list of waiting tasks
    """

    def __init__(self):
        self.active = None
        self.waiting = PriorityQueue()

    def execute(self, time):
        """
        Execute the scheduler for a certain time (Execute the active task if
        there is one).

        :param time: Time to compute
        :type time: int
        """

        if (self.active is not None):
            self.active.execute(time)

            if (self.active.finished()):
                self.active.finish()
            else :
                # Put the task back in the waiting list
                self.waiting.push(self.active, -self.active.priority())

        self.active = None

    def schedule(self):
        """
        Execute the most priority task on the scheduler.
        """

        if (not self.waiting.isEmpty()):
            task = self.waiting.pop()
            self.active = task

            # If it is the first start
            if (not task.started()):
                task.start()

    def printRunningTasks(self):
        ret = "WAITING : "
        for el in self.waitingTasks.list:
            ret += str(el[1]) + " "
        return ret

    def put(self, instance):
        """
        Put an instance on the scheduler in the waiting instances.

        :param instance: The instance
        :type instance: Instance
        """
        self.waiting.push(instance, -instance.priority())

if __name__ == "__main__":
    scheduler = Scheduler()

    t1 = HardTask(1, 0, 1, 5)
    t2 = HardTask(2, 0, 2, 10)
    t3 = HardTask(3, 1, 5, 5)
    
    htasks = InputParser()
    htasks.getTasksFromFile("test.csv")
    # print htasks.getHardTaskList()[2].idx

    list = EventList()
    populateEventList(htasks.getHardTaskList(), list)
    # populateEventList([t1, t2, t3], list)

    event = list.getNextEvent()
    i = 0
    while (event is not None):
        print "CURRENT :" + str(event)
        print list
        print scheduler.printRunningTasks()
        print 
        i = i + 1
        newEvent = scheduler.reactToEvent(event)
        if (newEvent is not None):
            list.insertEvent(newEvent)
        event = list.getNextEvent()
    print "Loops: " + str(i)
    
