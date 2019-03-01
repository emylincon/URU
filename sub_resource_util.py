from threading import Thread
import matplotlib.pyplot as plt
import psutil
import subprocess as sp
from drawnow import *
import time
import matplotlib.animation as animation

cpu = []
store = []
mem = []

fig = plt.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)


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
    cmd = ['df -t ext4 | grep {} | cut -d " " -f 13 | cut -c 1-2'.format(v_store)]
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

    plot_cpu()
    plot_mem()
    plot_storage()
    fig.suptitle('Resource Utilization (CPU|MEMORY|STORAGE)')


def plot_mem():
    global mem

    # ax1.clear()
    ax1.grid(True, color='k')
    ax1.plot(mem, linewidth=5, label='Memory')
    ax1.plot(calculate_mov_avg(mem), linewidth=5, label='Moving Avg Memory')
    ax1.set_ylabel('Utilization in percentage')
    #fig1.set_xlabel('Time (scale of 2 seconds)')
    ax1.set_title('Memory Utilization')
    ax1.legend()
    plt.subplot(ax1)


def plot_cpu():
    global cpu

    # ax2.clear()
    ax2.grid(True, color='k')
    ax2.plot(calculate_mov_avg(cpu), linewidth=5, label='Moving Avg CPU')
    ax2.plot(cpu, linewidth=5, label='CPU')

    #ax2.set_ylabel('Utilization in percentage')
    ax2.set_xlabel('Time (scale of 2 seconds)')
    ax2.set_title('CPU Utilization')
    ax2.legend()
    plt.subplot(ax2)


def plot_storage():
    global store

    # ax3.clear()
    ax3.grid(True, color='k')
    ax3.plot(store, linewidth=5, label='Storage')
    ax3.plot(calculate_mov_avg(store), linewidth=5, label='Moving Avg Storage')

    #ax3.set_ylabel('Utilization in percentage')
    # fig3.set_xlabel('Time (scale of 2 seconds)')
    ax3.set_title('Storage Utilization')
    ax3.legend()
    plt.subplot(ax3)


def main():
    global v_store

    cmd = ['df -t ext4 | grep sda1 | cut -d " " -f 13 | cut -c 1-2']
    st = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    if st == '':
        v_store = 'root'
    else:
        v_store = 'sda1'
    try:
        while True:
            get_resource_util()
            drawnow(plot_resource_util)
            time.sleep(2)
    except KeyboardInterrupt:
        print('Programme Terminated')


if __name__ == "__main__":
    main()


