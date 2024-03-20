import random

class Simulator:
   def __init__(self, average_arrival_rate, average_CPU_service_time, average_Disk_service_time, end_condition):
      self.average_arrival_rate = average_arrival_rate
      self.average_CPU_service_time = average_CPU_service_time
      self.average_Disk_service_time = average_Disk_service_time
      self.end_condition = end_condition

      self.clock = 0
      self.event_queue = []
      self.tasks_processed = 0
      