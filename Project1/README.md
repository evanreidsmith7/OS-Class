# CS4328: Project #1

## Overview

This project requires a significant amount of work and time, so please start early. Late submissions will incur a penalty of 10% per day for up to 2 days, after which they will not be accepted. Please read the description carefully and consult with me (preferably early) if you have any questions. Collaboration on ideas with other students is permitted, but your code and report must be your own work.

![Example Image](system.png)

### The Workload

Processes arrive at the CPU with an average arrival rate of λ (Lambda), following a Poisson distribution. If the CPU is idle, the process is processed immediately; otherwise, it joins the "Ready Queue". CPU service times are exponentially distributed, with an average service time of \(T_{s_{CPU}}\). A process exits with a 60% probability after CPU processing or moves to the Disk with a 40% probability for further service. Disk service times are also exponentially distributed, with an average service time of \(T_{s_{Disk}}\). Processes are served in a First-Come-First-Served (FCFS) order. See Figure 1 for an overview of the system components.

#### Performance Metrics

We aim to compute the following metrics for each experiment:

- The average turnaround time for processes that completed
- The average throughput (number of processes completed per unit time)
- The average CPU utilization
- The average Disk utilization
- The average number of processes in the CPU Ready queue
- The average number of processes in the Disk Queue

## The Simulator

The simulator will generate processes with unique IDs and arrival times. Arrival rates follow a Poisson distribution, and service times follow an exponential distribution. We will vary λ to simulate different workloads. The simulation ends after 10000 processes are completed, and the specified metrics should be reported.

Events (e.g., process arrivals, completions) trigger state updates in the simulator, managed through a priority "Event Queue". The simulator's clock updates with each event. Three command-line arguments are required: average arrival rate λ, average CPU service time, and average Disk service time.

## The Runs

Vary the average arrival rate λ from 1 to 30 processes per second. For each λ value, plot the specified metrics. It is recommended to automate these experiments with a batch file for easier result analysis.

## Submission Details

Submit through Canvas, including your code, compilation and execution instructions, and a report with results and their interpretation. Your program should run on the CS Linux servers via the command line. Indicate clearly how to compile and run your simulator.

**Grading:**

- 30%: Correct design and data structures
- 60%: Accurate results
- 10%: Documentation
