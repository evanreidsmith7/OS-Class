import sys
from DTEventSimulator import Simulator

if __name__ == "__main__":
   # Check if the correct number of arguments are provided
   if len(sys.argv) != 4:
      print("Usage: python main.py <average_arrival_rate> <average_CPU_service_time> <average_Disk_service_time>")
      print("Example: python main.py 12 .02 .06")
      sys.exit(1)  # Exit the script if the arguments are incorrect

   # Parse command-line arguments
   average_arrival_rate = float(sys.argv[1])
   average_CPU_service_time = float(sys.argv[2])
   average_Disk_service_time = float(sys.argv[3])

   if average_arrival_rate == 0:
      print("using defaults")
      # run the simulation with default values but varrying lambda 1 to 30
      for i in range(1, 31):
         sim = Simulator(i, average_CPU_service_time, average_Disk_service_time)
         # Run the simulation
         sim.run()
   else:
      sim = Simulator(average_arrival_rate, average_CPU_service_time, average_Disk_service_time)
      # Run the simulation
      sim.run()

