# This is a property of London South Bank University Developed by Emeka Ugwuanyi

from threading import Thread
import matplotlib.pyplot as plt
import psutil
import subprocess as sp
import time

cpu = []
store = []
mem = []


def get_cpu():
    prev_t = 0
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    # return delta     # Returns CPU util in percentage
    cpu.append(delta)


def get_mem():
    cmd = ['cat /proc/meminfo | grep MemFree |cut -d ":" -f 2 | cut -d "k" -f 1']
    free_mem = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    cmd = [' cat /proc/meminfo | grep MemAva |cut -d ":" -f 2 | cut -d "k" -f 1']
    total_mem = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    mem_util = (float(free_mem.strip()) / float(total_mem.strip())) * 100
    # return mem_util  # Returns memory util in percentage
    mem.append(mem_util)


def get_storage():
    cmd = ['df -t ext4 | grep sda1 | cut -d " " -f 13 | cut -c 1-2']
    storage = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    # return int(storage.strip())  # Returns storage in percentage
    store.append(float(storage.strip()))


def get_resource_util():
    h1 = Thread(target=get_mem)
    h2 = Thread(target=get_cpu)
    h3 = Thread(target=get_storage)

    h1.start()
    h2.start()
    h3.start()


def calculate_mov_avg(a1):
    ma1 = []  # moving average list
    avg1 = 0  # movinf average pointwise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count - 1) * avg1 + a1[i]) / count
        ma1.append(avg1)  # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def plot_resource_util():
    global mem
    global store
    global cpu

    fig1 = plt.figure('Utilization Plot')

    fig1 = plt.clf()
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(calculate_mov_avg(cpu), linewidth=5, label='CPU')
    fig1 = plt.plot(calculate_mov_avg(mem), linewidth=5, label='Memory')
    fig1 = plt.plot(calculate_mov_avg(store), linewidth=5, label='Storage')
    fig1 = plt.title('Resource Utilization')
    fig1 = plt.ylabel('Utilization in percentage')
    fig1 = plt.xlabel('Time (scale of 2 seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)


def main():
    try:
        while True:
            get_resource_util()
            plot_resource_util()
            plt.show()
            time.sleep(2)
    except:
        print('Error Occurred')


if __name__ == "__main__":
    main()


