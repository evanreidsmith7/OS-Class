import random
import math

###################################################################cpu#####################################
class CPU:
   def __init__(self):
      self.clock = 0
      self.busy = False
      self.current_process = Process()

###################################################################disk#####################################
class Disk:
   def __init__(self):
      self.busy = False
      self.current_process = Process()

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
      self.disk = Disk()
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = 10000

      self.ready_queue = []
      self.disk_queue = []
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
      elif self.cpu.busy is True and self.disk_probability <= 0.6:
         # cpu is busy and the process is not going to disk

         # add the process to the ready queue
         self.cpu.ready_queue.append(event.process)

      else:
         print("Something is wrong with the cpu")

      new_process = self.generateProcess()
      new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
      self.event_queue.append(new_arrival_event)


############################################################handleDisk#
   def handleDisk(self, event):
      pass

#######################################################handleDeparture#
   def handleDeparture(self, event):
      # process is done update metrics
      self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
      self.number_completed_processes += 1
      self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
      self.total_cpu_service_times += event.process.cpu_service_time
      
      # if ready queue is empty, cpu is idle
      if len(self.cready_queue) == 0:
         self.cpu.busy = False
      else:
         # pull the next process from the ready queue
         process_departing = self.ready_queue.pop(0)
         process_departing.start_time = self.cpu.clock
         process_departing.end_time = process_departing.start_time + process_departing.cpu_service_time
         new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
         self.event_queue.append(new_departure_event)


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
