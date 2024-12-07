from typing import List


class DeadlockDetector:
    def __init__(self, available: List[int], allocation: List[List[int]], request: List[List[int]]):
        self.available = available
        self.allocation = allocation
        self.request = request
        self.num_processes = len(allocation)
        self.num_resources = len(available)

    def detect_deadlock(self):
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []

        while True:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if all requests of process i can be satisfied
                    if all(self.request[i][j] <= work[j] for j in range(self.num_resources)):
                        # The process can finish
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True
                        print(f"Process {i} can finish. Updated work: {work}")
            if not found:
                break

        if all(finish):
            print("System is in a safe state.")
            print(f"Safe sequence: {safe_sequence}")
            return False, []  # No deadlock
        else:
            deadlocked_processes = [i for i, done in enumerate(finish) if not done]
            print("Deadlock detected!")
            print(f"Deadlocked processes: {deadlocked_processes}")
            return True, deadlocked_processes

    def recover_deadlock(self, deadlocked_processes: List[int]):
        # Simple recovery by terminating all deadlocked processes
        print("Recovering from deadlock by terminating deadlocked processes...")
        for process in deadlocked_processes:
            print(f"Terminating process {process} and releasing its resources.")
            for j in range(self.num_resources):
                self.available[j] += self.allocation[process][j]
                self.allocation[process][j] = 0
                self.request[process][j] = 0
        print(f"Available resources after recovery: {self.available}")


# Example Usage
if __name__ == "__main__":
    # Define Available resources
    available = [3, 3, 2]

    # Define Allocation matrix
    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]  # P4
    ]

    # Define Request matrix
    request = [
        [7, 4, 3],  # P0
        [1, 2, 2],  # P1
        [6, 0, 0],  # P2
        [0, 0, 0],  # P3
        [4, 3, 3]  # P4
    ]

    detector = DeadlockDetector(available, allocation, request)
    deadlock, deadlocked_procs = detector.detect_deadlock()

    if deadlock:
        detector.recover_deadlock(deadlocked_procs)
        # Re-check for deadlock after recovery
        detector.detect_deadlock()
