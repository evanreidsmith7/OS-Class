import random
import math

###################################################################cpu#####################################
class CPU:
   def __init__(self):
      self.clock = 0
      self.busy = False

###################################################################disk#####################################
class Disk:
   def __init__(self):
      self.busy = False

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
   def __init__(self, process=None):
      self.time = 0
      self.type = ''
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
      self.debug = False

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
      print(f"First process generated with PID={first_process.pid} and arrival time={first_process.arrival_time}\n\n") if self.debug else None
      first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)

      print(f"First event scheduled: Type={first_event.type}, Time={first_event.time}, Process PID={first_event.process.pid}\n\n") if self.debug else None
      self.event_queue.append(first_event)

      while self.number_completed_processes < self.end_condition:
         print("\n\n\n\n") if self.debug else None
         print(f"Current simulation clock: {self.cpu.clock}") if self.debug else None
         print(f"Number of completed processes: {self.number_completed_processes}") if self.debug else None
         print(f"Event queue size: {len(self.event_queue)}, Ready queue size: {len(self.ready_queue)}, Disk queue size: {len(self.disk_queue)}\n\n") if self.debug else None
         # sort the event queue so that the next occuring event appears
         self.event_queue.sort(key=lambda x: x.time)

         # take the next event from the event queue
         event = self.event_queue.pop(0)
         print(f"Processing event: Type={event.type}, Time={event.time}, Process PID={event.process.pid}\n\n\n\n") if self.debug else None


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
            print("Invalid event type") if self.debug else None
         
         print(f"\n\nPost-event processing: Simulation clock: {self.cpu.clock}, Ready queue size: {len(self.ready_queue)}, Disk queue size: {len(self.disk_queue)}") if self.debug else None

      avg_turn_around_time = (self.total_turnaround_time / self.end_condition)
      throughput = (self.end_condition / self.cpu.clock)
      cpu_utilization = 100 * (self.total_cpu_service_times / self.cpu.clock)
      disk_utilization = 100 * (self.total_disk_service_times / self.cpu.clock)
      avg_num_processes_in_readyQ = self.sum_num_of_proc_in_readyQ / self.end_condition
      avg_num_processes_in_diskQ = self.sum_num_of_proc_in_diskQ / self.end_condition

      self.report(avg_turn_around_time, throughput, cpu_utilization, disk_utilization, avg_num_processes_in_readyQ, avg_num_processes_in_diskQ)

##########################################################handleArrival#
   def handleArrival(self, event):
      print(f"Handling Arrival at time={self.cpu.clock}, Process ID={event.process.pid}, CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}\n\n") if self.debug else None
      if self.cpu.busy is False:
         self.cpu.busy = True
         depart_time = self.cpu.clock + event.process.cpu_service_time   
         departure_event = self.generateEvent(depart_time, "DEP", event.process)
         self.event_queue.append(departure_event)

         print(f"Scheduled Event DEP at time={departure_event.time}, Process ID={event.process.pid}\n\n\n\n") if self.debug else None
      else:
         self.ready_queue.append(event.process)
         print(f"Process ID={event.process.pid} added to ready queue\n\n\n\n") if self.debug else None
      
      if event.process.disk_done is False:
         self.num_disk_processes += 1
         new_process = self.generateProcess()
         new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
         self.event_queue.append(new_arrival_event)
         print(f"Scheduled next arrival at time={new_arrival_event.time}, Process ID={new_process.pid}\n\n\n\n") if self.debug else None

      '''
      # check if the process is done with disk
      if event.process.disk_done is False:
         self.num_disk_processes += 1
         # generate the next process
         new_process = self.generateProcess()
         new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
         self.event_queue.append(new_arrival_event)
         print(f"Scheduled next arrival at time={new_arrival_event.time}, Process ID={new_process.pid}\n\n\n\n") if self.debug else None
      '''

      # Log the state after handling the arrival
      print(f"Post-Arrival: CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}, Event Queue Size={len(self.event_queue)}\n\n") if self.debug else None

######################################################handleDiskArival#
   def handleDiskArival(self, event):
      print(f"Handling Disk Arrival at time={self.cpu.clock}, Process ID={event.process.pid}, Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}") if self.debug else None
      if self.disk.busy is False:
         # disk is not busy, process can be served
         self.disk.busy = True
         depart_time = self.cpu.clock + event.process.disk_service_time
         disk_departure_event = self.generateEvent(depart_time, "DISK_DEP", event.process)

         self.event_queue.append(disk_departure_event)
         print(f"Scheduled disk departure at time={disk_departure_event.time}, Process ID={event.process.pid}\n\n\n\n") if self.debug else None
      else:
         # disk is busy, process goes to disk queue
         self.disk_queue.append(event.process)
         print(f"Process ID={event.process.pid} added to disk queue\n\n\n\n") if self.debug else None
      print(f"Post-Disk Arrival: Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}, Event Queue Size={len(self.event_queue)}\n\n\n\n\n\n") if self.debug else None

###################################################handleDiskDeparture#
   def handleDiskDeparture(self, event):
      print(f"Handling Disk Departure at time={self.cpu.clock}, Process ID={event.process.pid}, Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}\n\n") if self.debug else None
      # process got served, take the service time
      self.total_disk_service_times += event.process.disk_service_time
      

      # schedule an arrival event for the process that just finished disk service
      event.process.disk_done = True
      cpu_arrival_time = self.cpu.clock
      cpu_arrival_event = self.generateEvent(cpu_arrival_time, "ARR", event.process)
      self.event_queue.append(cpu_arrival_event)

      if self.disk_queue: # if there are processes in the disk queue
         # schedule the next process in the disk queue
         self.disk.busy = True
         next_process = self.disk_queue.pop(0)
         
         depart_time = self.cpu.clock + next_process.disk_service_time
         disk_departure_event = self.generateEvent(depart_time, "DISK_DEP", next_process)
         self.event_queue.append(disk_departure_event)
         print(f"Scheduled next disk departure at time={disk_departure_event.time}, Process ID={next_process.pid}\n\n\n\n") if self.debug else None
      else:
         self.disk.busy = False
         print(f"Disk is now idle\n\n\n\n") if self.debug else None
      print(f"Post-Disk Departure: Disk Busy={self.disk.busy}, Disk Queue Size={len(self.disk_queue)}, Event Queue Size={len(self.event_queue)}\n\n\n\n") if self.debug else None

#######################################################handleDeparture#
   def handleDeparture(self, event):
      print(f"Handling CPU Departure at time={self.cpu.clock}, Process ID={event.process.pid}, CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}\n\n") if self.debug else None
      # process got served, take the service time
      self.total_cpu_service_times += event.process.cpu_service_time
      

      if random.uniform(0, 1) <= 0.6:
         self.number_completed_processes += 1
         self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
         print(f"Process ID={event.process.pid} completed at time={self.cpu.clock}\n\n\n\n") if self.debug else None
      else:
         disk_arrival_time = self.cpu.clock
         disk_arrival_event = self.generateEvent(disk_arrival_time, "DISK_ARR", event.process)
         self.event_queue.append(disk_arrival_event)
      
      if self.ready_queue:
         next_process = self.ready_queue.pop(0)
         self.cpu.busy = True
         depart_time = self.cpu.clock + next_process.cpu_service_time
         departure_event = self.generateEvent(depart_time, "DEP", next_process)
         self.event_queue.append(departure_event)
         print(f"Scheduled next departure at time={departure_event.time}, Process ID={next_process.pid}\n\n\n\n") if self.debug else None
      else:
         self.cpu.busy = False
         print(f"CPU is now idle\n\n\n\n") if self.debug else None

      print(f"Post-Departure: CPU Busy={self.cpu.busy}, Ready Queue Size={len(self.ready_queue)}, Completed Processes={self.number_completed_processes}\n\n\n\n") if self.debug else None

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
      event = Event(process=process)
      event.time = time
      event.type = type

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
