import threading
import time
import random

# Define buffer size
BUFFER_SIZE = 5

# Shared buffer
buffer = []

# Semaphores
mutex = threading.Semaphore(1)  # Controls access to the buffer
empty = threading.Semaphore(BUFFER_SIZE)  # Counts the empty slots in the buffer
full = threading.Semaphore(0)  # Counts the full slots in the buffer

def producer(producer_id):
    for _ in range(10):  # Each producer produces 10 items
        item = random.randint(1, 100)  # Produce an item (random number)

        # Wait for an empty slot
        empty.acquire()
        # Lock the buffer for access
        mutex.acquire()

        # Produce the item by adding it to the buffer
        buffer.append(item)
        print(f"Producer {producer_id} produced {item}. Buffer: {buffer}")

        # Release the lock and signal a full slot
        mutex.release()
        full.release()

        # Simulate production time
        time.sleep(random.uniform(0.1, 0.5))

def consumer(consumer_id):
    for _ in range(10):  # Each consumer consumes 10 items
        # Wait for a full slot
        full.acquire()
        # Lock the buffer for access
        mutex.acquire()

        # Consume the item by removing it from the buffer
        item = buffer.pop(0)
        print(f"Consumer {consumer_id} consumed {item}. Buffer: {buffer}")

        # Release the lock and signal an empty slot
        mutex.release()
        empty.release()

        # Simulate consumption time
        time.sleep(random.uniform(0.1, 0.5))

# Main function to create and start producer and consumer threads
def main():
    # Create producer and consumer threads
    producers = [threading.Thread(target=producer, args=(i,)) for i in range(2)]
    consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(2)]

    # Start all producers and consumers
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    # Wait for all producers and consumers to finish
    for p in producers:
        p.join()
    for c in consumers:
        c.join()

    print("All producers and consumers have finished.")

if __name__ == "__main__":
    main()
