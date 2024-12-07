import threading
import time
import tkinter as tk

# Shared variables for synchronization
N = 2
flag = [False] * N
turn = 0

# GUI setup
root = tk.Tk()
root.title("Producer-Consumer Simulation")
root.geometry("500x300")
root.configure(bg="#282C34")

# Define colors
bg_color = "#282C34"
text_color = "#FFFFFF"
critical_color = "#61AFEF"
non_critical_color = "#E06C75"

# Title Label
title_label = tk.Label(root, text="Producer-Consumer Simulation", font=("Helvetica", 16, "bold"), bg=bg_color, fg=text_color)
title_label.pack(pady=10)

# Frame for statuses
status_frame = tk.Frame(root, bg=bg_color)
status_frame.pack(pady=20)

# Producer Status
producer_label = tk.Label(status_frame, text="Producer", font=("Helvetica", 14), bg=bg_color, fg=critical_color)
producer_label.grid(row=0, column=0, padx=20)

producer_status_label = tk.Label(status_frame, text="Waiting", font=("Helvetica", 12, "bold"), width=20, bg=non_critical_color, fg=text_color)
producer_status_label.grid(row=0, column=1, padx=10)

# Consumer Status
consumer_label = tk.Label(status_frame, text="Consumer", font=("Helvetica", 14), bg=bg_color, fg=critical_color)
consumer_label.grid(row=1, column=0, padx=20)

consumer_status_label = tk.Label(status_frame, text="Waiting", font=("Helvetica", 12, "bold"), width=20, bg=non_critical_color, fg=text_color)
consumer_status_label.grid(row=1, column=1, padx=10)

# Function to update producer status in the GUI
def update_producer_status(status, color):
    root.after(0, lambda: producer_status_label.config(text=status, bg=color))

# Function to update consumer status in the GUI
def update_consumer_status(status, color):
    root.after(0, lambda: consumer_status_label.config(text=status, bg=color))

# Producer function
def producer(j):
    global turn
    while True:
        flag[j] = True
        turn = 1 - j
        while flag[1 - j] and turn == 1 - j:
            pass

        # Critical Section: Producer is producing
        update_producer_status("In Critical Section", critical_color)
        time.sleep(1)  # Simulate producing process

        # Exit Section
        flag[j] = False
        update_producer_status("Exited Critical Section", non_critical_color)
        time.sleep(1)  # Simulate remainder section

# Consumer function
def consumer(i):
    global turn
    while True:
        flag[i] = True
        turn = i
        while flag[1 - i] and turn == i:
            pass

        # Critical Section: Consumer is consuming
        update_consumer_status("In Critical Section", critical_color)
        time.sleep(2)  # Simulate consuming process

        # Exit Section
        flag[i] = False
        update_consumer_status("Exited Critical Section", non_critical_color)
        time.sleep(1)  # Simulate remainder section

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer, args=(0,))
consumer_thread = threading.Thread(target=consumer, args=(1,))

# Start the threads
producer_thread.start()
consumer_thread.start()

# Run the GUI main loop
root.mainloop()
