#!/usr/bin/env python

import sys
import time

import matplotlib.pyplot as plt
import psutil


class PidMonitor:
    def __init__(self, pid, mode):
        self.pid = int(pid)
        self.mode = mode
        file_mode = "w" if mode == "--monitor" else "r"
        self.monitor_log = open(f"monitor-pid-{pid}.log", file_mode)

    def monitor(self):
        proc = psutil.Process(self.pid)
        self.monitor_log.write("CPU\tRSS\tVMS\n")

        while proc.is_running():
            cpu = proc.cpu_percent()
            rss = proc.memory_info().rss / 1024**2
            vms = proc.memory_info().vms / 1024**2
            self.monitor_log.write(f"{cpu}\t{rss}\t{vms}\n")
            time.sleep(0.1)

        self.monitor_log.close()

    def plot(self):
        lines = self.monitor_log.readlines()
        self.monitor_log.close()

        lines = lines[2:]
        cpu_list = []
        rss_list = []  # physical memory
        vms_list = []  # virtual memory
        time_list = []
        for idx, line in enumerate(lines):
            cpu, rss, vms = line.split("\t")
            cpu_list.append(float(cpu))
            rss_list.append(float(rss))
            vms_list.append(float(vms))
            time_list.append(idx)

        # Plot CPU vs RSS
        fig, ax1 = plt.subplots()
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("cpu (%)", color="red")
        ax1.plot(time_list[::sampling], cpu_list[::sampling], color="red")
        ax1.set_title(f"sampling: {int(sampling*0.1)} s")
        ax2 = ax1.twinx()
        ax2.set_ylabel("physical memory (MB)", color="blue")
        ax2.plot(time_list[::sampling], rss_list[::sampling], color="blue")
        fig.tight_layout()
        fig.savefig(f"monitor-pid-{self.pid}-rss.png")

        # Plot CPU vs VMS
        fig, ax1 = plt.subplots()
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("cpu (%)", color="red")
        ax1.plot(time_list[::sampling], cpu_list[::sampling], color="red")
        ax1.set_title(f"sampling: {int(sampling*0.1)} s")
        ax2 = ax1.twinx()
        ax2.set_ylabel("virtual memory (MB)", color="blue")
        ax2.plot(time_list[::sampling], vms_list[::sampling], color="blue")
        fig.tight_layout()
        fig.savefig(f"monitor-pid-{self.pid}-vms.png")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "--monitor":
        pid = sys.argv[2]
        monitor = PidMonitor(pid, mode)
        monitor.monitor()
    elif mode == "--plot":
        pid = sys.argv[2]
        sampling = 10 if len(sys.argv) <= 3 else int(sys.argv[3]) * 10
        monitor = PidMonitor(pid, mode)
        monitor.plot()
    else:
        print(f"unknown mode: {mode}")
