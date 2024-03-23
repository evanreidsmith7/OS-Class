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
      self.clock = 0
      self.busy = False
      self.current_process = Process()
      self.queue = []

###################################################################process#####################################
class Process:
   def __init__(self):
      self.arrival_time = 0
      self.service_time = 0
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
   def __init__(self, average_arrival_rate, average_CPU_service_time, average_Disk_service_time, end_condition):
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = end_condition

      self.clock = 0
      self.event_queue = []
      self.completed_processes = 0

   def first_come_first_serve(self):
      # Implement the FCFS 
      print("Running the simulation")
      first_process = self.generateProcess()


   def generateProcess(self):
      process = Process()
      process.arrival_time = self.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.average_arrival_rate))

   #process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.lambda_val))
   #process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.avg_service_time))
         
   def run(self):
      self.first_come_first_serve()
