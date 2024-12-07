import threading
import time
import random

# Shared data
shared_data = 0

# Semaphores
resource_access = threading.Semaphore(1)  # Controls access to the shared resource
reader_count_access = threading.Semaphore(1)  # Controls access to the reader count
reader_count = 0  # Keeps track of the number of readers

def reader(reader_id):
    global reader_count, shared_data

    # Reader requests access to modify reader_count
    reader_count_access.acquire()
    reader_count += 1
    # If this is the first reader, lock the resource for reading
    if reader_count == 1:
        resource_access.acquire()
    reader_count_access.release()

    # Reading section
    print(f"Reader {reader_id} is reading the data: {shared_data}\n")
    time.sleep(random.uniform(0.1, 0.5))  # Simulate read time

    # Reader releases access
    reader_count_access.acquire()
    reader_count -= 1
    # If this is the last reader, release the resource for writers
    if reader_count == 0:
        resource_access.release()
    reader_count_access.release()

def writer(writer_id):
    global shared_data

    # Request exclusive access to the resource
    resource_access.acquire()

    # Writing section
    shared_data += 1  # Modify the shared data
    print(f"Writer {writer_id} has written data: {shared_data}")
    time.sleep(random.uniform(0.1, 0.5))  # Simulate write time

    # Release exclusive access to the resource
    resource_access.release()

# Main function to start reader and writer threads
def main():
    # Create reader and writer threads
    readers = [threading.Thread(target=reader, args=(i,)) for i in range(5)]
    writers = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

    # Start all threads
    for w in writers:
        w.start()
    for r in readers:
        r.start()

    # Wait for all threads to complete
    for w in writers:
        w.join()
    for r in readers:
        r.join()

if __name__ == "__main__":
    main()
