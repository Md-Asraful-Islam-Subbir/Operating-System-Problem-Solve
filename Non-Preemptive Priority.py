import matplotlib.pyplot as plt

# Number of processes
totalprocess = 5
# Process array [Arrival Time, Burst Time, Priority, Process Number]
proc = [[0 for _ in range(4)] for _ in range(totalprocess)]

# Function to calculate waiting time (WT) and turnaround time (TAT)
def get_wt_time(wt, stime):
    # Calculate the waiting time for each process
    for i in range(totalprocess):
        wt[i] = stime[i] - proc[i][0]  # Waiting Time = Start Time - Arrival Time
        if wt[i] < 0:
            wt[i] = 0  # Ensure no negative waiting time

def get_tat_time(tat, wt):
    # Turnaround time = Completion Time - Arrival Time
    for i in range(totalprocess):
        tat[i] = proc[i][1] + wt[i]  # Turnaround Time = Burst Time + Waiting Time

def findgc():
    stime = [0] * totalprocess
    ctime = [0] * totalprocess

    # First process' start time and completion time
    stime[0] = proc[0][0]
    ctime[0] = stime[0] + proc[0][1]

    # Calculate start time and completion time for other processes
    for i in range(1, totalprocess):
        stime[i] = max(ctime[i - 1], proc[i][0])  # Start time = max(Previous completion time, Current arrival time)
        ctime[i] = stime[i] + proc[i][1]  # Completion time = Start time + Burst time

    wt = [0] * totalprocess
    tat = [0] * totalprocess
    wavg, tavg = 0, 0

    # Calculate waiting time and turnaround time
    get_wt_time(wt, stime)
    get_tat_time(tat, wt)

    print("Process\tArrival Time\tBurst Time\tStart Time\tComplete Time\tTurnaround Time\tWaiting Time")
    for i in range(totalprocess):
        wavg += wt[i]
        tavg += tat[i]
        print(f"P{proc[i][3]}\t\t\t{proc[i][0]}\t\t\t{proc[i][1]}\t\t\t{stime[i]}\t\t\t{ctime[i]}\t\t\t\t{tat[i]}\t\t\t\t\t{wt[i]}")

    print("\nAverage waiting time:", wavg / totalprocess)
    print("Average turnaround time:", tavg / totalprocess)

    # Generate Gantt Chart
    plotGanttChart(stime, ctime)

def plotGanttChart(stime, ctime):
    fig, gnt = plt.subplots(figsize=(10, 4))

    gnt.set_title("Gantt Chart for Scheduling")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    yticks = [15 * (i + 1) for i in range(totalprocess)]
    labels = [f"P{proc[i][3]}" for i in range(totalprocess)]
    gnt.set_yticks(yticks)
    gnt.set_yticklabels(labels)

    for i in range(totalprocess):
        gnt.broken_barh([(stime[i], ctime[i] - stime[i])], (yticks[i] - 5, 10),
                        facecolors=('tab:blue' if i % 2 == 0 else 'tab:orange'))

    plt.show()

# Driver code
if __name__ == "__main__":
    arrivaltime = [1, 2, 3, 4, 5]
    bursttime = [3, 5, 1, 7, 4]
    priority = [3, 4, 1, 7, 8]

    for i in range(totalprocess):
        proc[i][0] = arrivaltime[i]
        proc[i][1] = bursttime[i]
        proc[i][2] = priority[i]
        proc[i][3] = i + 1

    # Sorting processes by arrival time
    proc = sorted(proc, key=lambda x: x[0])

    # Generate Gantt Chart and calculate times
    findgc()
