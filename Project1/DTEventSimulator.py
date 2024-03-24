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
   last_pid = 0  
   def __init__(self):
      self.arrival_time = 0
      self.cpu_service_time = 0
      self.disk_service_time = 0
      self.cpu_done = False
      self.disk_done = False

      self.pid = Process.last_pid + 1  # Assign a unique PID to the process
      Process.last_pid = self.pid  # Update the last assigned PID

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
      self.end_condition = 10000

      self.ready_queue = []
      self.disk_queue = []
      self.event_queue = []

      self.num_disk_processes = 0
      self.number_completed_processes = 0
      self.total_turnaround_time = 0
      self.total_cpu_service_times = 0
      self.total_disk_service_times = 0
      self.sum_num_of_proc_in_readyQ = 0
      self.sum_num_of_proc_in_diskQ = 0

#################################################first_come_first_serve#
   def first_come_first_serve(self):
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
      
      avg_turn_around_time = (self.total_turnaround_time / self.end_condition)
      throughput = (self.end_condition / self.cpu.clock)
      cpu_utilization = 100 * (self.total_cpu_service_times / self.cpu.clock)
      disk_utilization = 100 * (self.total_disk_service_times / self.cpu.clock)
      avg_num_processes_in_readyQ = self.sum_num_of_proc_in_readyQ / self.end_condition
      avg_num_processes_in_diskQ = self.sum_num_of_proc_in_diskQ / self.end_condition

      self.report(avg_turn_around_time, throughput, cpu_utilization, disk_utilization, avg_num_processes_in_readyQ, avg_num_processes_in_diskQ)

##########################################################handleArrival#
   def handleArrival(self, event):
      if self.cpu.busy is False:
         # cpu isnt busy and the process is not going to disk
         # start the process on the cpu (cpu.busy true) 
         self.cpu.busy = True
         disk_probability = float(random.uniform(0, 1))
         event.type = "DEP" if disk_probability <= 0.6 else "DISK_ARR"
         event.time = self.cpu.clock + event.process.cpu_service_time
         self.event_queue.append(event)

      elif self.cpu.busy is True:
         print("cpu is busy, Process going to ready queue\n\n")
         # cpu is busy and the process is not going to disk
         # add the process to the ready queue
         self.ready_queue.append(event.process)

      else:
         print("Something is wrong with the cpu\n\n")

      # check if the process is done with disk
      if event.process.disk_done is False:
         self.num_disk_processes += 1
         # generate the next process
         new_process = self.generateProcess()
         new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
         self.event_queue.append(new_arrival_event)

######################################################handleDiskArival#
   def handleDiskArival(self, event):
      self.cpu.busy = False
      if self.disk.busy is False:
         # disk isnt busy
         self.disk.busy = True
         
         event.type = "DISK_DEP"
         # update the event time to when its done getting service with disk
         event.time = self.cpu.clock + event.process.disk_service_time
         # add the event back to the event queue
         self.event_queue.append(event)

      elif self.disk.busy is True:
         # disk is busy
         # add the process to the disk queue
         self.disk_queue.append(event.process)
      
      else:
         print("Something is wrong with the disk")

###################################################handleDiskDeparture#
   def handleDiskDeparture(self, event):
      # process is done with disk update metrics
      self.sum_num_of_proc_in_diskQ += len(self.disk_queue)
      self.total_disk_service_times += event.process.disk_service_time

      # change the event to an arrival event since it is going to the cpu
      event.type = "ARR"
      event.time = self.cpu.clock
      # set disk done to true so another process doesn't get generated
      event.process.disk_done = True 
      self.event_queue.append(event)

      # if disk queue is empty, disk is idle
      if len(self.disk_queue) == 0:
         self.disk.busy = False
      else:
         # pull the next process from the disk queue
         process_departing = self.disk_queue.pop(0)
         depart_time = self.cpu.clock + process_departing.disk_service_time
         new_departure_event = self.generateEvent(depart_time, "DISK_DEP", process_departing)
         self.event_queue.append(new_departure_event)

#######################################################handleDeparture#
   def handleDeparture(self, event):
      # process is done update metrics
      turnaround_time = self.cpu.clock - event.process.arrival_time

      self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
      self.number_completed_processes += 1
      self.total_turnaround_time += turnaround_time
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
      cpu_lambda = 1.0 / self.average_CPU_service_time
      disk_lambda = 1.0 / self.average_Disk_service_time
      process.cpu_service_time = math.log(1 - float(random.uniform(0, 1))) / (-cpu_lambda)
      process.disk_service_time = math.log(1 - float(random.uniform(0, 1))) / (-disk_lambda)
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

##############################################################report#
   def report(self, avg_turn_around_time, throughput, cpu_utilization, disk_utilization, avg_num_processes_in_readyQ, avg_num_processes_in_diskQ):
      print(f"{'Metrics Report':^40}")
      print(f"{'='*40}")
      print(f"{'Throughput:':<30}{throughput:>10.4f} processes/unit time")      
      print(f"{'CPU Utilization:':<30}{cpu_utilization:>10.4f}%")
      print(f"{'Disk Utilization:':<30}{disk_utilization:>10.4f}%")
      print(f"{'Avg. Processes in Ready Queue:':<30}{avg_num_processes_in_readyQ:>10.4f}")
      print(f"{'Avg. Processes in Disk Queue:':<30}{avg_num_processes_in_diskQ:>10.4f}")
      print(f"{'Avg. Turnaround Time:':<30}{avg_turn_around_time:>10.4f} seconds")
      print(f"{'='*40}")

      print('\n\n\n')

      print(f"{'Compare to':^40}")
      print(f"{'='*40}")
      print(f"{'Throughput:':<30}{12} processes/unit time")      
      print(f"{'CPU Utilization:':<30}{40}%")
      print(f"{'Disk Utilization:':<30}{48}%")
      print(f"{'Avg. Processes in Ready Queue:':<30}{0.2666}")
      print(f"{'Avg. Processes in Disk Queue:':<30}{0.44}")
      print(f"{'Avg. Turnaround Time:':<30}{0.132} seconds")
      print(f"{'='*40}")

      print('\n\n\n')

      print("calculated average_cpu_service_time", self.total_cpu_service_times / self.end_condition)
      print("calculated average_disk_service_time", self.total_disk_service_times / self.num_disk_processes)
###################################################################simulator#####################################
