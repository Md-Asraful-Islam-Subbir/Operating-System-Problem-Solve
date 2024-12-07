import matplotlib.pyplot as plt

def findWaitingTime(processes, n, bt, wt):
    wt[0] = 0  # waiting time for first process is 0
    for i in range(1, n):
        wt[i] = bt[i - 1] + wt[i - 1]

def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]

def findavgTime(processes, n, bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0

    findWaitingTime(processes, n, bt, wt)
    findTurnAroundTime(processes, n, bt, wt, tat)

    print("Processes    Burst time    Waiting time    Turn around time")
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        print(f" {processes[i]}\t\t\t\t {bt[i]}\t\t\t\t {wt[i]}\t\t\t\t {tat[i]}")

    print("\nAverage waiting time =", (total_wt / n))
    print("Average turn around time =", (total_tat / n))

    # Plotting the Waiting Time and Turnaround Time using matplotlib
    plotTimes(processes, bt, wt, tat)

def plotTimes(processes, bt, wt, tat):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Plot Waiting Time
    ax[0].bar(processes, wt, color='skyblue')
    ax[0].set_title("Waiting Time for Each Process")
    ax[0].set_xlabel("Processes")
    ax[0].set_ylabel("Waiting Time")

    # Plot Turnaround Time
    ax[1].bar(processes, tat, color='salmon')
    ax[1].set_title("Turnaround Time for Each Process")
    ax[1].set_xlabel("Processes")
    ax[1].set_ylabel("Turnaround Time")

    plt.show()

# Driver code
if __name__ == "__main__":
    processes = [1, 2, 3,4,5,6,]
    n = len(processes)
    priority=[2,1,4,2,3,2]
    burst_time = [15, 20, 20, 20, 5, 15]
    arrivalTime=[0,0,20,25,45,55]

    findavgTime(processes, n, burst_time)
