import threading
import time
import random
import tkinter as tk

# Shared data and semaphore definitions
shared_data = 0
resource_access = threading.Semaphore(1)  # Controls access to the shared resource
reader_count_access = threading.Semaphore(1)  # Controls access to the reader count
reader_count = 0  # Tracks the number of readers

# Shared status for readers and writers
reader_status = [""] * 5
writer_status = [""] * 2

# GUI setup
root = tk.Tk()
root.title("Readers-Writers Problem")
root.geometry("600x400")
root.configure(bg="#282C34")

# Define colors
bg_color = "#282C34"
text_color = "#FFFFFF"
reader_color = "#61AFEF"
writer_color = "#E06C75"
default_color = "#ABB2BF"

# Title Label
title_label = tk.Label(root, text="Readers-Writers Simulation", font=("Helvetica", 16, "bold"), bg=bg_color, fg=text_color)
title_label.pack(pady=10)

# Shared data display
shared_data_label = tk.Label(root, text="Shared Data: 0", font=("Helvetica", 14), bg=bg_color, fg=text_color)
shared_data_label.pack(pady=10)

# Status frames for readers and writers
status_frame = tk.Frame(root, bg=bg_color)
status_frame.pack(pady=20)

# Reader status display
reader_status_labels = []
for i in range(5):
    label = tk.Label(status_frame, text=f"Reader {i}: ", font=("Helvetica", 12), width=25, bg=default_color, fg=text_color)
    label.grid(row=i, column=0, padx=10, pady=2)
    reader_status_labels.append(label)

# Writer status display
writer_status_labels = []
for i in range(2):
    label = tk.Label(status_frame, text=f"Writer {i}: ", font=("Helvetica", 12), width=25, bg=default_color, fg=text_color)
    label.grid(row=i, column=1, padx=10, pady=2)
    writer_status_labels.append(label)

# Function to update shared data in GUI
def update_shared_data():
    shared_data_label.config(text=f"Shared Data: {shared_data}")

# Periodic function to refresh GUI status
def refresh_status():
    # Update the GUI labels based on the current status
    for i in range(5):
        reader_status_labels[i].config(text=f"Reader {i}: {reader_status[i]}", bg=reader_color if reader_status[i] == "Reading" else default_color)

    for i in range(2):
        writer_status_labels[i].config(text=f"Writer {i}: {writer_status[i]}", bg=writer_color if writer_status[i] == "Writing" else default_color)

    # Update shared data
    update_shared_data()

    # Schedule the next GUI update
    root.after(100, refresh_status)

# Reader function
def reader(reader_id):
    global reader_count, shared_data

    while True:
        # Request access to modify reader count
        reader_count_access.acquire()
        reader_count += 1
        if reader_count == 1:
            resource_access.acquire()
        reader_count_access.release()

        # Reading section
        reader_status[reader_id] = "Reading"
        print(f"Reader {reader_id} is reading the data: {shared_data}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate read time

        # Release access
        reader_count_access.acquire()
        reader_count -= 1
        if reader_count == 0:
            resource_access.release()
        reader_count_access.release()

        reader_status[reader_id] = ""  # Clear status when done reading
        time.sleep(random.uniform(0.5, 1))  # Simulate wait time between reads

# Writer function
def writer(writer_id):
    global shared_data

    while True:
        # Request exclusive access to the resource
        resource_access.acquire()

        # Writing section
        shared_data += 1
        writer_status[writer_id] = "Writing"
        print(f"Writer {writer_id} has written data: {shared_data}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate write time

        # Release exclusive access
        resource_access.release()

        writer_status[writer_id] = ""  # Clear status when done writing
        time.sleep(random.uniform(0.5, 1))  # Simulate wait time between writes

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

# Start the main function in a background thread
threading.Thread(target=main).start()

# Start refreshing the status display in the GUI
refresh_status()

# Run the GUI main loop
root.mainloop()
