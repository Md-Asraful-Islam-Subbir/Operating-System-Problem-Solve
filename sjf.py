import matplotlib.pyplot as plt


def main():
    # Taking the number of processes
    n = int(input("Enter number of processes: "))
    # Matrix for storing Process Id, Burst Time, Waiting Time & Turnaround Time.
    A = [[0 for j in range(4)] for i in range(n)]
    total_wt, total_tat = 0, 0

    print("Enter Burst Time:")
    for i in range(n):  # User Input Burst Time and assigning Process Id.
        A[i][1] = int(input(f"P{i + 1}: "))
        A[i][0] = i + 1

    # Sorting processes by Burst Time
    for i in range(n):
        index = i
        for j in range(i + 1, n):
            if A[j][1] < A[index][1]:
                index = j
        A[i], A[index] = A[index], A[i]  # Swapping rows

    # Calculating Waiting Times
    A[0][2] = 0  # First process has 0 waiting time
    for i in range(1, n):
        A[i][2] = sum(A[j][1] for j in range(i))  # Summing burst times of previous processes
        total_wt += A[i][2]

    avg_wt = total_wt / n  # Average waiting time

    # Calculating Turnaround Time and displaying the results
    print("P     BT     WT     TAT")
    for i in range(n):
        A[i][3] = A[i][1] + A[i][2]  # TAT = BT + WT
        total_tat += A[i][3]
        print(f"P{A[i][0]}     {A[i][1]}     {A[i][2]}      {A[i][3]}")

    avg_tat = total_tat / n  # Average turnaround time
    print(f"Average Waiting Time= {avg_wt}")
    print(f"Average Turnaround Time= {avg_tat}")

    # Plotting the Waiting Time and Turnaround Time
    plotTimes(A, n)


def plotTimes(A, n):
    processes = [A[i][0] for i in range(n)]
    burst_times = [A[i][1] for i in range(n)]
    waiting_times = [A[i][2] for i in range(n)]
    turnaround_times = [A[i][3] for i in range(n)]

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Plot Waiting Time
    ax[0].bar(processes, waiting_times, color='skyblue')
    ax[0].set_title("Waiting Time for Each Process")
    ax[0].set_xlabel("Process ID")
    ax[0].set_ylabel("Waiting Time (WT)")

    # Plot Turnaround Time
    ax[1].bar(processes, turnaround_times, color='salmon')
    ax[1].set_title("Turnaround Time for Each Process")
    ax[1].set_xlabel("Process ID")
    ax[1].set_ylabel("Turnaround Time (TAT)")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()


#62834