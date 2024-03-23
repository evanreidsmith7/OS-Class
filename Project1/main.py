import sys
from DTEventSimulator import Simulator

if __name__ == "__main__":
   # Check if the correct number of arguments are provided
   if len(sys.argv) != 4:
      print("Usage: python main.py <average_arrival_rate> <average_CPU_service_time> <average_Disk_service_time>")
      sys.exit(1)  # Exit the script if the arguments are incorrect

   # Parse command-line arguments
   average_arrival_rate = float(sys.argv[1])
   average_CPU_service_time = float(sys.argv[2])
   average_Disk_service_time = float(sys.argv[3])

   # Total number of processes to simulate
   end_condition = 10000

   # Initialize the simulator with the provided command-line arguments
   sim = Simulator(average_arrival_rate, average_CPU_service_time, average_Disk_service_time)

   # Run the simulation
   sim.run()

   # Generate the report
   sim.generateReport()