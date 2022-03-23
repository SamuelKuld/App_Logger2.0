import time
import psutil
import pickle


def get_process_exes():
    names = []
    for process in psutil.process_iter():
        time.sleep(.1)
        try:
            names.append(process.exe())
        except:
            continue
    return names


class Process():
    def __init__(self, process):
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

    def save_status(self):
        with open("pickled.dat", "wb+") as file:
            pickle.dump(self.processes, file)
        with open("INFO.txt", "w+") as file:
            previous_path = ""
            for process in self.processes:
                for setting in self.settings:
                    if (process.path == setting or setting == "All") and previous_path != process.path:
                        file.write(f"{process.name} = {process.runtime}\n")
                        previous_path = process.path

        self.update_process_list()

    def load_status(self):
        try:
            with open("pickled.dat", "rb+") as file:
                self.processes = pickle.load(file)
        except:
            self.update_process_list()

    def __init__(self, settings=[]):
        self.update_process_list()
        self.settings = settings

    def remove_redundant_names(self):
        old_name = ""
        new_processes = []
        for process in self.processes:
            if process.name == old_name:
                continue
            new_processes.append(process)
            old_name = process.name
        self.processes = new_processes

    def remove_redundant_paths(self):
        old_path = ""
        new_processes = []
        for process in self.processes:
            if process.path == old_path:
                continue
            new_processes.append(process)
            old_path = process.path
        self.processes = new_processes


class Settings():
    def __init__(self):
        with open("settings.txt") as data:
            file_data = data.read()
        self.settings = file_data.split("\n")


def main():
    settings = Settings()
    processes = Processes(settings.settings)
    processes.load_status()
    while 1:
        start = time.time()
        processes_to_change = []
        current_processes = get_process_exes()
        previous_name = ""
        for i, process in enumerate(processes.processes):
            time.sleep(.01)
            if (
                    process.path in current_processes
                    and previous_name != process.name):
                processes_to_change.append(i)
                previous_name = process.name
        for i in processes_to_change:
            processes.processes[i].runtime += time.time() - start
        processes.save_status()


if __name__ == '__main__':
    main()
