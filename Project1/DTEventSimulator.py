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
            self.handle_arrival(event)
         elif event.type == "DISK":
            self.handle_disk(event)
         elif event.type == "DEP":
            self.handle_departure(event)
         else:
            print("Invalid event type")


def handle_arrival(self, event):
   pass

def handle_disk(self, event):
   pass

def handle_departure(self, event):
   pass


   def generateProcess(self):
      process = Process()

      process.arrival_time = self.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.average_arrival_rate))
      process.cpu_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_CPU_service_time))
      process.disk_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_Disk_service_time))
      process.end_time = process.arrival_time + process.cpu_service_time
      process.start_time = 0

      return process
      
   def generateEvent(self, time, type, process):
      event = Event()
      event.time = time
      event.type = type
      event.process = process

      return event
      

   def run(self):
      # start fcfs scheduler
      self.first_come_first_serve()
