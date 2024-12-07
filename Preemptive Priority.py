import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid        # Process ID
        self.arrival = arrival # Arrival Time
        self.burst = burst     # Burst Time
        self.priority = priority # Priority
        self.remaining_time = burst # Remaining Burst Time (for preemption)
        self.completion = 0     # Completion Time
        self.waiting = 0        # Waiting Time
        self.turnaround = 0     # Turnaround Time

# Function to perform Preemptive Priority Scheduling
def preemptive_priority_scheduling(processes):
    time = 0
    complete = 0
    n = len(processes)
    schedule = []  # Gantt chart timeline (tuples of (process id, start time, duration))

    while complete != n:
        # Select the process with the highest priority that has arrived and is incomplete
        highest_priority_process = None
        for p in processes:
            if p.arrival <= time and p.remaining_time > 0:
                if highest_priority_process is None or p.priority < highest_priority_process.priority:
                    highest_priority_process = p

        if highest_priority_process is not None:
            start_time = time
            highest_priority_process.remaining_time -= 1
            time += 1

            # Record process execution for the Gantt chart
            if len(schedule) > 0 and schedule[-1][0] == highest_priority_process.pid:
                # Extend the previous segment if it's the same process
                schedule[-1] = (schedule[-1][0], schedule[-1][1], schedule[-1][2] + 1)
            else:
                # Add a new segment
                schedule.append((highest_priority_process.pid, start_time, 1))

            # Check if the process is now complete
            if highest_priority_process.remaining_time == 0:
                highest_priority_process.completion = time
                highest_priority_process.turnaround = highest_priority_process.completion - highest_priority_process.arrival
                highest_priority_process.waiting = highest_priority_process.turnaround - highest_priority_process.burst
                complete += 1
        else:
            # No process available, idle CPU
            schedule.append((-1, time, 1))  # -1 indicates an idle time slot
            time += 1

    return schedule

# Function to print and calculate average times
def print_avg_times(processes):
    total_waiting = 0
    total_turnaround = 0

    print("\nProcess\tArrival\tBurst\tPriority\tWaiting\tTurnaround")
    for p in processes:
        total_waiting += p.waiting
        total_turnaround += p.turnaround
        print(f"{p.pid}\t\t{p.arrival}\t\t{p.burst}\t\t{p.priority}\t\t\t{p.waiting}\t\t\t{p.turnaround}")

    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

# Function to visualize the Gantt chart with unique colors for each process
def plot_gantt_chart(schedule):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_title("Gantt Chart - Preemptive Priority Scheduling")
    ax.set_xlabel("Time")
    ax.set_yticks([1])
    ax.set_yticklabels(["CPU"])

    # Generate a unique color for each process
    colors = list(mcolors.TABLEAU_COLORS.keys())  # Using Tableau colors for uniqueness
    process_colors = {pid: colors[i % len(colors)] for i, pid in enumerate(set(pid for pid, _, _ in schedule if pid != -1))}

    # Plot each segment of the Gantt chart
    for pid, start, duration in schedule:
        if pid != -1:
            # Use unique color for each process
            color = process_colors[pid]
            ax.broken_barh([(start, duration)], (0.9, 0.2), facecolors=(color))
            ax.text(start + duration / 2, 1, f"P{pid}", ha='center', va='center', color='white')
        else:
            # For idle time, use grey color
            ax.broken_barh([(start, duration)], (0.9, 0.2), facecolors='grey')
            ax.text(start + duration / 2, 1, "Idle", ha='center', va='center', color='black')

    plt.show()

# Driver code
if __name__ == "__main__":
    # Input the processes (process_id, arrival_time, burst_time, priority)
    processes = [
        Process(1, 0, 7, 2),
        Process(2, 2, 4, 1),
        Process(3, 4, 1, 3),
        Process(4, 5, 4, 2)
    ]

    # Execute the scheduling algorithm
    schedule = preemptive_priority_scheduling(processes)

    # Print results
    print_avg_times(processes)

    # Plot the Gantt chart
    plot_gantt_chart(schedule)
