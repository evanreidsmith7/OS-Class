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
      self.cpu_service_time = 0
      self.disk_service_time = 0
      self.cpu_done = False
      self.disk_done = False
      self.disk_probability = 0.0

###################################################################event#####################################
class Event:
   def __init__(self):
      self.time = 0
      self.type = ''
      self.process = Process()

###################################################################simulator#####################################
class Simulator:
   def __init__(self, average_arrival_rate, average_CPU_service_time, average_Disk_service_time):
      self.cpu = CPU()
      self.disk = Disk()
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = 10

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
         elif event.type == "DISK_ARR":
            self.handleDiskArival(event)
         elif event.type == "DISK_DEP":
            self.handleDiskDeparture(event)
         elif event.type == "DEP":
            self.handleDeparture(event)
         else:
            print("Invalid event type")
      
      print("Simulation complete")

##########################################################handleArrival#
   def handleArrival(self, event):
      if self.cpu.busy is False:
         # cpu isnt busy and the process is not going to disk

         # start the process on the cpu (cpu.busy true) 
         self.cpu.busy = True

         # check if the process is going to disk
         if event.process.disk_probability <= 0.6:
            print("Process Departing after cpu service")
            # change the event to a depart because it will leave the cpu
            event.type = "DEP"
            # update the event time to when its done getting service with cpu
            event.time = self.cpu.clock + event.process.cpu_service_time

            # add the event back to the event queue
            self.event_queue.append(event)
         else:
            print("Process going to disk after cpu service")
            # change the event to disk because it will go to disk
            event.type = "DISK_ARR"
            # update the event time to when its done getting service with cpu
            event.time = self.cpu.clock + event.process.cpu_service_time

            # add the event back to the event queue
            self.event_queue.append(event)

      elif self.cpu.busy is True:
         print("cpu is busy, Process going to ready queue")
         # cpu is busy and the process is not going to disk
         # add the process to the ready queue
         self.ready_queue.append(event.process)

      else:
         print("Something is wrong with the cpu")

      new_process = self.generateProcess()
      new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
      self.event_queue.append(new_arrival_event)


######################################################handleDiskArival#
   def handleDiskArival(self, event):
      if self.disk.busy is False:
         # disk isnt busy
         print("disk is not busy, process Departing Disk after disk service")
         self.disk.busy = True
         
         #change the event to an arrival because it will arrive back to the cpu
         event.type = "DISK_DEP"
         # update the event time to when its done getting service with disk
         event.time = self.cpu.clock + event.process.disk_service_time

         # add the event back to the event queue
         self.event_queue.append(event)

      elif self.disk.busy is True:
         print("disk is busy, Process going to disk queue")
         # disk is busy
         # add the process to the disk queue
         self.disk_queue.append(event.process)
      
      else:
         print("Something is wrong with the disk")

###################################################handleDiskDeparture#
   def handleDiskDeparture(self, event):
      print("Process Departed from disk, pulling next process from disk queue if available")
      # process is done with disk update metrics
      self.sum_num_of_proc_in_diskQ += len(self.disk_queue)
      self.total_disk_service_times += event.process.disk_service_time

      # if disk queue is empty, disk is idle
      if len(self.disk_queue) == 0:
         self.disk.busy = False
      else:
         # pull the next process from the disk queue
         process_departing = self.disk_queue.pop(0)
         depart_time = self.cpu.clock + process_departing.disk_service_time
         new_departure_event = self.generateEvent(depart_time, "ARR", process_departing)
         self.event_queue.append(new_departure_event)

#######################################################handleDeparture#
   def handleDeparture(self, event):
      print("Process Departed from cpu, pulling next process from ready queue if available")
      # process is done update metrics
      self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
      self.number_completed_processes += 1
      self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
      self.total_cpu_service_times += event.process.cpu_service_time
      
      # if ready queue is empty, cpu is idle
      if len(self.ready_queue) == 0:
         self.cpu.busy = False
      else:
         # pull the next process from the ready queue
         process_departing = self.ready_queue.pop(0)
         depart_time = self.cpu.clock + process_departing.cpu_service_time
         new_departure_event = self.generateEvent(depart_time, "DEP", process_departing)
         self.event_queue.append(new_departure_event)

#######################################################generateProcess#
   def generateProcess(self):
      process = Process()

      process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.average_arrival_rate))
      process.cpu_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_CPU_service_time))
      process.disk_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_Disk_service_time))
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
