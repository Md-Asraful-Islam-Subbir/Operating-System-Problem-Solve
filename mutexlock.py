import threading
import time

# Each thread will count TIMES_TO_COUNT times
TIMES_TO_COUNT = 21000

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

def thread_routine(counter):
    # Each thread starts here
    tid = threading.current_thread().ident
    # Print the count before this thread starts iterating.
    # In order to read the value of count, we lock the mutex:
    with counter.lock:
        print(f"Thread [{tid}]: Count at thread start = {counter.count}")
    for i in range(TIMES_TO_COUNT):
        # Iterate TIMES_TO_COUNT times
        # Increment the counter at each iteration
        # Lock the mutex for the duration of the incrementation
        counter.increment()
    # Print the final count when this thread finishes its own count,
    # without forgetting to lock the mutex:
    with counter.lock:
        print(f"Thread [{tid}]: Final count = {counter.count}")

def main():
    # Structure containing the threads' total count:
    counter = Counter()

    # Since each thread counts TIMES_TO_COUNT times and that
    # we have 2 threads, we expect the final count to be
    # 2 * TIMES_TO_COUNT:
    print(f"Main: Expected count is {2 * TIMES_TO_COUNT}")
    # Thread creation:
    t1 = threading.Thread(target=thread_routine, args=(counter,))
    print(f"Main: Created first thread [{t1.ident}]")
    t2 = threading.Thread(target=thread_routine, args=(counter,))
    print(f"Main: Created second thread [{t2.ident}]")
    # Thread starting:
    t1.start()
    t2.start()
    # Thread joining:
    t1.join()
    print(f"Main: Joined first thread [{t1.ident}]")
    t2.join()
    print(f"Main: Joined second thread [{t2.ident}]")
    # Final count evaluation:
    # (Here we can read the count without worrying about
    # the lock because all threads have been joined and
    # there can be no data race between threads)
    if counter.count != (2 * TIMES_TO_COUNT):
        print(f"Main: ERROR! Total count is {counter.count}")
    else:
        print(f"Main: OK. Total count is {counter.count}")

if __name__ == "__main__":
    main()