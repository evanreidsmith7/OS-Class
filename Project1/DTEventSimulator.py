import random
class CPU:
   def __init__(self):
      self.clock = 0
      self.busy = False
      self.current_process = Process()
      self.ready_queue = []

class Disk:
   def __init__(self):
      self.clock = 0
      self.busy = False
      self.current_process = Process()
      self.queue = []

class Process:
   def __init__(self):
      self.arrival_time = 0
      self.service_time = 0
      self.cpu_service_time = 0
      self.disk_service_time = 0
      self.cpu_done = False
      self.disk_done = False

class Event:
   def __init__(self, time, type, process):
      self.time = time
      self.type = type
      self.process = process

class Simulator:
   def __init__(self, average_arrival_rate, average_CPU_service_time, average_Disk_service_time, end_condition):
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = end_condition

      self.clock = 0
      self.event_queue = []
      self.tasks_processed = 0
   
   def first_come_first_serve(self):
      # Implement the FCFS 
      print("Running the simulation")


#process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.lambda_val))
#process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.avg_service_time))
      
def run(self):
   self.first_come_first_serve()
