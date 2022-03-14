import os
import time
import psutil
import pickle


def get_process_exes():
    names = []
    for process in psutil.process_iter():
        try:
            names.append(process.exe())
        except:
            continue

    return names


class Process():
    def __init__(self, process):
        self.process = process
        try:
            self.name = process.name()
            self.process_id = process.pid
            self.path = process.exe()
            self.runtime = 0
        except:
            self.name = None
            self.process_id = None
            self.path = None
            self.runtime = 0

    def set_pid(self, pid):
        self.process_id = pid

    def __repr__(self):
        return f"{'{'}\n  Name : {self.name}\n  Path : {self.path}\nruntime : {self.runtime}\n{'}'}\n\n"

    def __str__(self):
        return f"{'{'}\n  Name : {self.name}\n  Path : {self.path}\n  {self.runtime}\n{'}'}\n\n"


class Processes():
    def update_process_list(self):
        self.processes = []
        for process in psutil.process_iter():
            self.processes.append(Process(process))

    def is_process_running(self, process_name: str):
        for process_name_i in get_process_exes():
            if process_name == process_name_i:
                return True
        return False

    def save_status(self):
        with open("pickled.dat", "wb+") as file:
            pickle.dump(self.processes, file)

    def load_status(self):
        with open("pickled.dat", "rb+") as file:
            self.processes = pickle.load(file)

    def __init__(self):
        self.update_process_list()


class Settings():
    def __init__(self):
        with open("settings") as data:
            file_data = data.read()
        self.settings = file_data.split("\n")


def main():
    settings = Settings()
    processes = Processes()
    while 1:
        start = time.time()
        current_processes = get_process_exes()
        for process in processes.processes:
            if process.path in settings.settings and process.path in current_processes:
                process.runtime += time.time() - start
                print(process.runtime)

        print("---")


if __name__ == '__main__':
    main()
