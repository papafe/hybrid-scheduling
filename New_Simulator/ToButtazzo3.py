import sys
import json
from numpy import arange, linspace
from Task import PeriodicTask, AperiodicTask
from Server import PollingServer, DeferrableServer, BackgroundServer
from Simulator import Simulator
from Instance import Instance, DeadLineException
from copy import deepcopy
from time import time
from numpy import arange
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_FOLDER = "results_q1/"
filename = '../CaseStudies/ts2.json'

PERIODIC_LOADS = arange(0.1, 0.8, 0.1)
MAX_TOTAL_LOAD = 0.60 #maximum total load considered
MIN_AP_LOAD = 0.01 #minimum aperiodic load
NUM_POINTS = 9 # number of points to consider for the aperiodic load range
MAX_AP_LOAD = 0.70
until = 2500000


def computeAverage(filename):
    fi = open(filename, 'r')
    somma = 0.0
    total_comp_ap = 0.0
    n = 0.0
    lines = fi.readlines()[3:-3]
    #print lines, filename
    for line in lines:
        line_split = line.split('|')
        if line_split[1] != '  HARD':
            n = n+1
            finish = float(line_split[4])
            start = float(line_split[2])

            somma = somma + (finish-start)
            total_comp_ap = total_comp_ap + float(line_split[5])
    return somma/n, total_comp_ap/n





def simulationLoop(server, capacity, period, scaled, ex_time, int_time):
        name = server + ".csv"
        s = Simulator(stats = name)

        # Set the server
        if server == 'polling':
            s.server = PollingServer(capacity, period)
        elif server == 'deferrable':
            s.server = DeferrableServer(capacity, period)
        else:
            s.server = BackgroundServer()


        # Load the taskset
        for t in scaled:
            s.tasks.append(t)

        # Create the aperiodic task
        ap = AperiodicTask("Soft", ex_time, int_time)
        s.tasks.append(ap)


        # RUUUUUUUUN !!!
        s.init(until)
        s.run()


        return computeAverage(name)

res = dict()
start = time()
file = open(filename, 'rb')
data = json.load(file)
taskset = list()
periodics = data["periodics"]
for t in periodics:
    taskset.append(PeriodicTask(t["id"], t["wcet"], t["period"]))
    
res = dict()
res["polling"] = list()
res["deferrable"] = list()

for p_load in PERIODIC_LOADS:
    res[p_load] = dict()

    # Scale the task set
    scaled = deepcopy(list(taskset))
    for t in scaled:
        t.wcet = t.wcet * p_load

    # Compute the execution time
    #until = PeriodicTask.lcm(scaled)*NUM_HYPERPERIODS
    print "HYPERPERIOD", PeriodicTask.lcm(scaled)
    res[p_load]['pol'] = dict()
    res[p_load]['def'] = dict()
    res[p_load]['bac'] = dict()

    # Compute variables for the server
    util = PollingServer.util(p_load)
    util_def = DeferrableServer.util2(p_load)

    period = 18
    #period = min([t.period for t in scaled])*1
    capacity = util * period
    capacity_def = util_def * period

    print "\nPERIODIC LOAD: " + str(p_load),
    print "\tUTIL POLLING: " + str(util),
    print "\tUTIL DEFERRABLE: " + str(util_def)
    print "*"*40


    if util_def <= 0 or util_def > 1.0:
        util_def = 0



    APERIODIC_LOAD = linspace(MIN_AP_LOAD, MAX_AP_LOAD, NUM_POINTS)

    ap_load = 0.95 - p_load
    int_time = 18
    ex_time = int_time * ap_load

    print "\nAPERIODIC LOAD: " + str(ap_load),
    print "\t\tEXECUTION TIME: " + str(ex_time)
    min_util = util
    max_util = 1.0
    cur = min_util

    while max_util - min_util > 0.01:
        try :
            capacity = cur * period
            for i in range(0,5):
                simulationLoop('polling', capacity, period, scaled, ex_time, int_time)
            min_util = (max_util + min_util) / 2
            cur = min_util
        except DeadLineException:
            max_util = (max_util + min_util) / 2
            cur = max_util
    print "Polling : " + str(min_util)
    res["polling"].append(min_util)
    
    min_util = util_def
    max_util = 1.0
    cur = min_util
    while max_util - min_util > 0.01:
        try :
            capacity = cur * period
            avp = simulationLoop('deferrable', capacity, period, scaled, ex_time, int_time)
            min_util = (max_util + min_util) / 2
            cur = min_util
        except DeadLineException:
            max_util = (max_util + min_util) / 2
            cur = max_util
    print "Deferrable : " + str(min_util)
    res["deferrable"].append(min_util)
    #res[p_load]['pol'][ap_load] = avp[0]

    #avd = simulationLoop('deferrable', capacity_def, period, scaled, ex_time, int_time)
    #res[p_load]['def'][ap_load] = avd[0]

    #avb = simulationLoop('background', capacity, period, scaled, ex_time, int_time)
    #res[p_load]['bac'][ap_load] = avb[0]

    #print "POL: " +str(avp[0]) + "\tDEF: " +str(avd[0]) + "\tBAC: " +str(avb[0])



print "ELAPSED TIME: ",  time() - start
fi = open("bounds3.json",'w')
json.dump(res,fi)

plt.plot(PERIODIC_LOADS, res["polling"], "g")
plt.plot(PERIODIC_LOADS, res["deferrable"], "b")

plt.savefig("bounds3.svg")
