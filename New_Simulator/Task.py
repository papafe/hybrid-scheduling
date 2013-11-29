from Instance import Instance
from Event import Event
from numpy import random

class Task(object):
    def __init__(self, id):
        self.id = id

    def generateEvents(self, until):
        """
        Compute the events for a simulation until the given time.
        """
        pass

class PeriodicTask(Task):
    def __init__(self, id, wcet, period):
        Task.__init__(self, id)
        self.priority = 1.0/float(period)
        self.wcet = wcet
        self.period = period

    def generateEvents(self, until):
        events = list()
        i = int(random.uniform(0, self.period))
        while i < until:
            instance = Instance(Instance.HARD, self, i, self.wcet, self.priority)
            event = Event(Event.ARRIVAL, i, instance)
            events.append(event)
            i += self.period

        return events

class AperiodicTask(Task):
    def __init__(self, id, computation, release):
        """
        Init the task.
        release : The mean interarrival time
        computation : The mean computation time
        """
        Task.__init__(self, id)
        self.computation = computation
        self.release = release
        self.priority = 0

    def generateEvents(self, until):
        events = list()
        i = random.poisson(1.0/self.release)
        while i < until:
            computation = random.exponential(1.0/self.computation)
            instance = Instance(Instance.SOFT, self, i, self.computation, self.priority)
            event = Event(Event.ARRIVAL, i, instance)
            events.append(event)
            i += random.poisson(1.0/self.release)
        return events
