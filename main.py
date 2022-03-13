"""
    Version 2.0.0
    Ideally, we're working with one datatype in order to determine the processes
    That's the Process Class.


    In order to initialize a list of processes, we need to make sure that we have one to compare from
    We'll store that in memory through data serialization.
    In order to preserve the integrity of the structure of the files, we'll have an initializer function.
    I went ahead and made another function that allowed me to just grab the pickle of the data.

    In the main function we need to initialize and then grab an old list of processes to append to and add to.
    Then, we need to add all the new processes to the list of old processes and finally take that and add an incriment of time to each process in the result list.
    
    Chicken
    
"""

import os
import time 
import psutil
import pickle

class Process():
    def __init__(self, path : str, ):
        self.path = path
        self.name = path.split()[-1]
        self.runtime = 0
        self.extra_info = {}

    def __repr__(self):
        return f"{'{'}\n  Name : {self.name}\n  Path : {self.path}\nruntime : {self.runtime}\n{'}'}\n\n"

    def __str__(self):
        return f"{'{'}\n  Name : {self.name}\n  Path : {self.path}\n  {self.runtime}\n{'}'}\n\n"

def get_all_individual_processes(): # Individual processes since it removes repeat processes
    list_of_Processes = []
    list_of_individual_processes = []
    for process in psutil.process_iter():
        try:
            process_path = process.exe()
            if process_path not in list_of_individual_processes:
                list_of_Processes.append(Process(process_path))
                list_of_individual_processes.append(process_path)
        except:
            continue
    return list_of_Processes


def initialize():
    if "process_list.dat" not in os.listdir():
        with open("process_list.dat", "wb+") as file:
            pickle.dump(get_all_individual_processes(), file);
    else:
        print("Nominal file structure")


def get_old_processes():
    with open("process_list.dat", "rb") as file:
        data = pickle.load(file)
    return data


def add_time_to_processes(list_of_processes, time_to_add):
    for process in list_of_processes:
        process.runtime += time_to_add
    return list_of_processes


def add_processes_to_old_processes(list_of_processes, old_processes):
    old_process_paths = [path.path for path in old_processes]
    for new_process in list_of_processes:
        if new_process.path not in old_process_paths:
            old_processes.append(new_process)
        else:
            old_processes # Need to set old process equal to new process in order to update it
    return old_processes 


def dump_processes(processes):
    with open("process_list.dat", "wb+") as file:
        pickle.dump(processes, file)
    with open("processes_readable.txt", "w+") as file:
        readable = ''
        for process in processes:
            readable = readable + str(process)
        file.write(readable)



def main(test=False):
    initialize()
    old_processes = get_old_processes()
    while True:
        start = time.time()
        


if __name__ == '__main__':
    main(test=True)