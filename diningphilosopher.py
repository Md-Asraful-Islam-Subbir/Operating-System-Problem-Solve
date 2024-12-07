import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, id, left_chopstick, right_chopstick):
        threading.Thread.__init__(self)
        self.id = id
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self):
        for _ in range(5):  # Each philosopher will try to eat 5 times
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.id} is thinking.")
        time.sleep(random.uniform(1, 3))  # Simulate thinking time

    def eat(self):
        # Asymmetric solution: odd philosophers pick left chopstick first, even pick right first
        first, second = (self.left_chopstick, self.right_chopstick) if self.id % 2 == 0 else (self.right_chopstick, self.left_chopstick)

        # Try to pick up first chopstick
        first.acquire()
        print(f"Philosopher {self.id} picked up first chopstick.")
        time.sleep(0.1)  # Wait a moment to increase chance of context switch

        # Try to pick up second chopstick
        second.acquire()
        print(f"Philosopher {self.id} picked up second chopstick.")

        # Eating
        print(f"Philosopher {self.id} is eating.")
        time.sleep(random.uniform(1, 2))  # Simulate eating time

        # Release both chopsticks
        first.release()
        print(f"Philosopher {self.id} released first chopstick.")
        second.release()
        print(f"Philosopher {self.id} released second chopstick.")

def dining_philosophers(num_philosophers):
    # Initialize chopsticks (locks)
    chopsticks = [threading.Lock() for _ in range(num_philosophers)]

    # Initialize philosophers
    philosophers = [Philosopher(i, chopsticks[i], chopsticks[(i + 1) % num_philosophers]) for i in range(num_philosophers)]

    # Start each philosopher's thread
    for philosopher in philosophers:
        philosopher.start()

    # Wait for all philosophers to finish
    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    num_philosophers = 5
    dining_philosophers(num_philosophers)
