import time
from typing import Type
import psutil
import pickle


class Process:
    def __init__(self, process, time_running=0):
        self.time_running = time_running
        self.process = process
        self.name = process.name()

    def __str__(self):
        return f"{self.name} : {self.time_running}"


def get_running_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            print(proc.name())
            processes.append(Process(proc))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes


def get_running_process_names():
    processes = []
    for proc in psutil.process_iter():
        processes.append(proc.name())
    return processes


def get_pickled():
    try:
        with open("pickled.dat", "rb") as f:
            processes = pickle.load(f)
        return processes
    except FileNotFoundError:
        return None


class Processes():
    def __init__(self):
        self.processes = get_pickled()
        if self.processes == None:
            self.processes = get_running_processes()

    def save_processes(self):
        with open('processes.txt', 'w+') as f:
            f.write("")
        with open('processes.txt', 'a+') as f:
            for process in self.processes:
                f.write(str(process) + "\n")

        # serialize processes
        with open("pickled.dat", "wb+") as f:
            pickle.dump(self.processes, f)

    def add_to_running_processes(self, amount_of_time):
        self.already_running_processes = get_running_processes()
        self.already_added = []
        for process in self.already_running_processes:
            if (process not in self.processes):
                self.processes.append(
                    Process(process.process, time_running=amount_of_time))
            if (process.name in self.already_running_processes and
                    process.name not in self.already_added):
                process.time_running += amount_of_time


def main_loop():
    processes = Processes()
    while True:
        start = time.time()
        processes.add_to_running_processes(time.time() - start)
        processes.save_processes()


if __name__ == '__main__':
    main_loop()
