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
      self.disk_probability = 0.0

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
      print(f"First process generated with PID={first_process.pid} and arrival time={first_process.arrival_time}")

      first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
      print(f"First event scheduled: Type={first_event.type}, Time={first_event.time}, Process PID={first_event.process.pid}")
      self.event_queue.append(first_event)

      while self.number_completed_processes < self.end_condition:
         print(f"Current simulation clock: {self.cpu.clock}")
         print(f"Number of completed processes: {self.number_completed_processes}")
         print(f"Event queue size: {len(self.event_queue)}, Ready queue size: {len(self.ready_queue)}, Disk queue size: {len(self.disk_queue)}")
         
         # sort the event queue so that the next occuring event appears
         self.event_queue.sort(key=lambda x: x.time)

         # take the next event from the event queue
         event = self.event_queue.pop(0)
         print(f"Processing event: Type={event.type}, Time={event.time}, Process PID={event.process.pid}")


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
         
         print(f"Post-event processing: Simulation clock: {self.cpu.clock}, Ready queue size: {len(self.ready_queue)}, Disk queue size: {len(self.disk_queue)}")
      
      print("Simulation complete. Final metrics:")
      print(f"Total completed processes: {self.number_completed_processes}")
      print(f"Average turnaround time: {self.total_turnaround_time / self.number_completed_processes if self.number_completed_processes > 0 else 0}")
      print(f"CPU utilization: {(self.total_cpu_service_times / self.cpu.clock) * 100 if self.cpu.clock > 0 else 0}%")
      print(f"Disk utilization: {(self.total_disk_service_times / self.cpu.clock) * 100 if self.cpu.clock > 0 else 0}%")

##########################################################handleArrival#
   def handleArrival(self, event):
      print(f"Handling Arrival at time={self.cpu.clock}, Process ID={event.process.id}, CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}")
      if self.cpu.busy is False:
         # cpu isnt busy and the process is not going to disk
         # start the process on the cpu (cpu.busy true) 
         self.cpu.busy = True
         event_action = "departing" if event.process.disk_probability <= 0.6 else "going to disk"
         event.type = "DEP" if event.process.disk_probability <= 0.6 else "DISK_ARR"
         event.type = self.cpu.clock + event.process.cpu_service_time

         print(f"Process {event_action} after CPU service. Scheduling {event.type} event at time={event.time}")
         self.event_queue.append(event)

      elif self.cpu.busy is True:
         print("cpu is busy, Process going to ready queue")
         # cpu is busy and the process is not going to disk
         # add the process to the ready queue
         self.ready_queue.append(event.process)

      else:
         print("Something is wrong with the cpu")

      # Log the state after handling the arrival
      print(f"Post-Arrival: CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}, Event Queue Size={len(self.event_queue)}")

      new_process = self.generateProcess()
      new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
      self.event_queue.append(new_arrival_event)
      print(f"Scheduled next arrival at time={new_arrival_event.time}, Process ID={new_process.id}")

######################################################handleDiskArival#
   def handleDiskArival(self, event):
      print(f"Handling Disk Arrival at time={self.cpu.clock}, Process ID={event.process.pid}, Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}")

      if self.disk.busy is False:
         # disk isnt busy
         print("disk is not busy, process Departing Disk after disk service")
         self.disk.busy = True
         
         #change the event to an arrival because it will arrive back to the cpu
         event.type = "DISK_DEP"
         # update the event time to when its done getting service with disk
         event.time = self.cpu.clock + event.process.disk_service_time
         print(f"Disk is not busy, scheduling {event.type} for Process ID={event.process.pid} at time={event.time}")
         # add the event back to the event queue
         self.event_queue.append(event)

      elif self.disk.busy is True:
         print(f"Disk is busy, adding Process ID={event.process.pid} to the disk queue")
         # disk is busy
         # add the process to the disk queue
         self.disk_queue.append(event.process)
      
      else:
         print("Something is wrong with the disk")

      print(f"Post-Disk Arrival: Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}, Event Queue Size={len(self.event_queue)}")
###################################################handleDiskDeparture#
   def handleDiskDeparture(self, event):
      print(f"Handling Disk Departure at time={self.cpu.clock}, Process ID={event.process.pid}, Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}")
      # process is done with disk update metrics
      self.sum_num_of_proc_in_diskQ += len(self.disk_queue)
      self.total_disk_service_times += event.process.disk_service_time

      # if disk queue is empty, disk is idle
      if len(self.disk_queue) == 0:
         self.disk.busy = False
         print(f"Disk queue is empty after Process ID={event.process.pid} departure, Disk is now idle.")
      else:
         # pull the next process from the disk queue
         process_departing = self.disk_queue.pop(0)
         depart_time = self.cpu.clock + process_departing.disk_service_time
         new_departure_event = self.generateEvent(depart_time, "ARR", process_departing)
         self.event_queue.append(new_departure_event)
         print(f"Process ID={process_departing.pid} pulled from disk queue for service. Scheduling DISK_DEP event at time={depart_time}")
      
      print(f"Post-Disk Departure: Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}, Event Queue Size={len(self.event_queue)}")

#######################################################handleDeparture#
   def handleDeparture(self, event):
      print(f"Handling CPU Departure at time={self.cpu.clock}, Process ID={event.process.pid}, CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}")

      # process is done update metrics
      turnaround_time = self.cpu.clock - event.process.arrival_time

      self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
      self.number_completed_processes += 1
      self.total_turnaround_time += turnaround_time
      self.total_cpu_service_times += event.process.cpu_service_time
      print(f"Process ID={event.process.pid} departed. Turnaround time: {turnaround_time}, CPU service time: {event.process.cpu_service_time}")      
      
      # if ready queue is empty, cpu is idle
      if len(self.ready_queue) == 0:
         self.cpu.busy = False
         print("Ready queue is empty. CPU set to idle.")
      else:
         # pull the next process from the ready queue
         process_departing = self.ready_queue.pop(0)
         depart_time = self.cpu.clock + process_departing.cpu_service_time

         print(f"Next process ID={process_departing.pid} pulled from ready queue. Scheduled departure at time={depart_time}")
        
         new_departure_event = self.generateEvent(depart_time, "DEP", process_departing)
         self.event_queue.append(new_departure_event)
      
      print(f"Post-Departure: CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}, Completed Processes={self.number_completed_processes}")

#######################################################generateProcess#
   def generateProcess(self):
      process = Process()

      process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.average_arrival_rate))
      process.cpu_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_CPU_service_time))
      process.disk_service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_Disk_service_time))
      #process.disk_probability = random.uniform(0, 1)
      process.disk_probability = 0
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
