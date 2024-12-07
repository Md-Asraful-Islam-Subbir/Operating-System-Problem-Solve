import threading
import time

N = 2
flag = [False] * N
turn = 0


# Producer function
def producer(j):
    global turn
    while True:
        flag[j] = True
        turn = 1 - j
        while flag[1 - j] and turn == 1 - j:
            # Wait for the consumer to finish
            pass

        # Critical Section: Producer is producing
        print("Producer is in the critical section.")
        time.sleep(1)  # Simulate producing process (1 second)

        # Exit Section
        flag[j] = False  # Producer is out of the critical section
        print("Producer exited the critical section.\n")

        time.sleep(1)  # Simulate remainder section (non-critical section work)


# Consumer function
def consumer(i):
    global turn
    while True:
        flag[i] = True
        turn = i
        while flag[1 - i] and turn == i:
            pass

        # Critical Section: Consumer is consuming
        print("Consumer is in the critical section.")
        time.sleep(2)  # Simulate consuming process (2 seconds)

        # Exit Section: Consumer finished consuming
        flag[i] = False  # Consumer is out of the critical section
        print("Consumer exited the critical section.\n")

        time.sleep(1)  # Simulate remainder section (non-critical section work)


# Create producer and consumer threads
producer_thread = threading.Thread(target=producer, args=(0,))
consumer_thread = threading.Thread(target=consumer, args=(1,))

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for the threads to finish (this won't actually happen, as they run in an infinite loop)
producer_thread.join()
consumer_thread.join()
