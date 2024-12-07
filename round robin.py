import matplotlib.pyplot as plt

def findWaitingTime(processes, n, bt, wt, quantum):
    rem_bt = [bt[i] for i in range(n)]
    t = 0  # Current time

    gantt_chart = []  # To store the Gantt chart details

    while True:
        done = True
        for i in range(n):
            if rem_bt[i] > 0:
                done = False  # There is a pending process

                if rem_bt[i] > quantum:
                    # Process a quantum time slice
                    t += quantum
                    rem_bt[i] -= quantum
                    gantt_chart.append((processes[i], t - quantum, t))

                else:
                    # Process for remaining burst time
                    t += rem_bt[i]
                    wt[i] = t - bt[i]
                    gantt_chart.append((processes[i], t - rem_bt[i], t))
                    rem_bt[i] = 0

        if done:
            break

    return gantt_chart  # Return Gantt chart for visualization


def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]


def findavgTime(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n

    # Get waiting time and Gantt chart
    gantt_chart = findWaitingTime(processes, n, bt, wt, quantum)

    # Get turnaround time
    findTurnAroundTime(processes, n, bt, wt, tat)

    # Display process details
    print("Processes    Burst Time     Waiting Time    Turn-Around Time")
    total_wt, total_tat = 0, 0
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        print(f"  {processes[i]}            {bt[i]}              {wt[i]}              {tat[i]}")

    print("\nAverage waiting time = %.5f" % (total_wt / n))
    print("Average turn around time = %.5f" % (total_tat / n))

    # Plot Gantt Chart
    plotGanttChart(gantt_chart)


def plotGanttChart(gantt_chart):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_title("Gantt Chart - Round Robin Scheduling")
    ax.set_xlabel("Time")
    ax.set_yticks([10])
    ax.set_yticklabels(['CPU'])

    for process, start, end in gantt_chart:
        ax.broken_barh([(start, end - start)], (9, 2),
                       facecolors=('tab:blue' if process % 2 == 0 else 'tab:orange'))
        ax.text(start + (end - start) / 2, 10, f"P{process}", ha='center', va='center', color='white')

    plt.show()


# Driver code
if __name__ == "__main__":
    # Process IDs
    proc = [1, 2, 3]
    n = len(proc)

    # Burst times
    burst_time = [10, 5, 8]

    # Time quantum
    quantum = 2
    findavgTime(proc, n, burst_time, quantum)
