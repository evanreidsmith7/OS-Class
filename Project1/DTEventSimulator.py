import random
import math

###################################################################cpu#####################################
class CPU:
   def __init__(self):
      self.clock = 0
      self.busy = False
      self.current_process = Process()
      self.ready_queue = []

###################################################################disk#####################################
class Disk:
   def __init__(self):
      self.busy = False
      self.current_process = Process()
      self.disk_queue = []

###################################################################process#####################################
class Process:
   def __init__(self):
      self.arrival_time = 0
      self.start_time = 0
      self.end_time = 0
      self.cpu_service_time = 0
      self.disk_service_time = 0
      self.cpu_done = False
      self.disk_done = False
      self.disk_probability = 0.0

###################################################################event#####################################
class Event:
   def __init__(self, time, type, process):
      self.time = time
      self.type = type
      self.process = process

###################################################################simulator#####################################
class Simulator:
   def __init__(self, average_arrival_rate, average_CPU_service_time, average_Disk_service_time):
      self.cpu = CPU()
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = 10000

      self.event_queue = []
      self.number_completed_processes = 0
      self.total_turnaround_time = 0
      self.total_cpu_service_times = 0
      self.total_disk_service_times = 0
      self.sum_num_of_proc_in_readyQ = 0
      self.sum_num_of_proc_in_diskQ = 0

#################################################first_come_first_serve#
   def first_come_first_serve(self):
      # Implement the FCFS 
      print("Running the scheduler...")
      first_process = self.generateProcess()

      first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
      self.event_queue.append(first_event)

      while self.number_completed_processes < self.end_condition:
         # sort the event queue so that the next occuring event appears
         self.event_queue.sort(key=lambda x: x.time)

         # take the next event from the event queue
         event = self.event_queue.pop(0)

         # set clock to the occuring event time because time hops around
         self.cpu.clock = event.time

         # check the type of event
         # cpu arrival: ARR, disk arival: DISK, departure: DEP
         if event.type == "ARR":
            self.handleArrival(event)
         elif event.type == "DISK":
            self.handleDisk(event)
         elif event.type == "DEP":
            self.handleDeparture(event)
         else:
            print("Invalid event type")

##########################################################handleArrival#
   def handleArrival(self, event):
      if self.cpu.busy is False and self.disk_probability <= 0.6:
         # cpu isnt busy and the process is not going to disk
         # start the process on the cpu (cpu.busy true) 
         self.cpu.busy = True
         # change the event to a depart because it will leave the cpu
         event.type = "DEP"
         event.process.end_time = self.cpu.clock + event.process.cpu_service_time
         # update the event time to the end time of the process
         event.time = event.process.end_time

         # add the event back to the event queue
         self.event_queue.append(event)
      else:
         print("Something is wrong with the cpu")


############################################################handleDisk#
   def handleDisk(self, event):
      pass

#######################################################handleDeparture#
   def handleDeparture(self, event):
      pass

#######################################################generateProcess#
   def generateProcess(self):
      process = Process()

      process.arrival_time = self.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.average_arrival_rate))
      process.cpu_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_CPU_service_time))
      process.disk_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_Disk_service_time))
      process.end_time = process.arrival_time + process.cpu_service_time
      process.start_time = 0
      process.disk_probability = random.uniform(0, 1)

      return process
   
#######################################################generateEvent#
   def generateEvent(self, time, type, process):
      event = Event()
      event.time = time
      event.type = type
      event.process = process

      return event

###############################################################run#
   def run(self):
      # start fcfs scheduler
      self.first_come_first_serve()
###################################################################simulator#####################################
