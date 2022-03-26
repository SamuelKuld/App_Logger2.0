import pickle
from time import time
import psutil


def get_process_names():
    return [proc.name() for proc in psutil.process_iter()]


class Process():
    def __init__(self, name, time_running=0):
        self.time_running = time_running
        self.name = name

    def add_to_time(self, amount_of_time):
        self.time_running += amount_of_time


class Processes():
    def __init__(self):
        self.processes = []

    def load_processes(self, process_names):
        for name in process_names:
            self.processes.append(Process(name))

    # Save processes to file method
    def save_processes_to_file(self):
        pickle.dump(self.processes, open("pickled.dat", "wb+"))

    def load_processes_from_file(self):
        try:
            self.load_processes(pickle.load(open("pickled.dat", "rb")))
        except:
            self.save_processes_to_file()

    def compare_processes(self, new_processes):
        for process in self.processes:
            if process.name not in new_processes:
                new_processes.append(process)

    def add_to_times(self, amount_of_time):
        for process in self.processes:
            if process.name in get_process_names():
                process.add_to_time(amount_of_time)

    def __str__(self):
        process_string = ""
        for process in self.processes:
            process_string += process.name + ": " + \
                str(process.time_running) + "\n"

        return process_string


# Main loop that iterates through the processes and adds time to each process
processes = Processes()
start_time = time()
while True:
    processes.load_processes(get_process_names())
    processes.compare_processes(get_process_names())
    processes.add_to_times(time() - start_time)
    print(processes)
    processes.load_processes_from_file()
    start_time = time()
