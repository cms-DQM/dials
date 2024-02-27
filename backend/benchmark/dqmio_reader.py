# flake8: noqa

import sys

sys.path.insert(0, "../")

from dials.dqmio_etl.reader import DQMIOReader
from tqdm import tqdm


class HistIngestion:
    H1D_VALID_MES = (3, 4, 5)
    H2D_VALID_MES = (6, 7, 8)

    def __init__(self, fpath: str) -> None:
        self.reader = DQMIOReader(fpath)

    def __h1d(self):
        for run, lumi in tqdm(self.reader.list_lumis()):
            h1d_list = []
            me_list = self.reader.get_mes_for_lumi(run, lumi, "*")

            for me in me_list:
                if me.type not in self.H1D_VALID_MES:
                    continue

                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(
                    hist_x_bins + 1
                )  # Takes low edge of overflow bin instead.
                data = [me.data.GetBinContent(i) for i in range(1, hist_x_bins + 1)]
                h1d_list.append(
                    dict(
                        title=me.name,
                        entries=entries,
                        data=data,
                        x_min=hist_x_min,
                        x_max=hist_x_max,
                        x_bin=hist_x_bins,
                    )
                )

            # print(f'Run #{run} / Lumi #{lumi} / h1d_list len: {len(h1d_list)}')

    def __h2d(self):
        for run, lumi in tqdm(self.reader.list_lumis()):
            h2d_list = []
            me_list = self.reader.get_mes_for_lumi(run, lumi, "*")
            for me in me_list:
                if me.type not in self.H2D_VALID_MES:
                    continue

                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_y_bins = me.data.GetNbinsY()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins) + me.data.GetXaxis().GetBinWidth(hist_x_bins)
                hist_y_min = me.data.GetYaxis().GetBinLowEdge(1)
                hist_y_max = me.data.GetYaxis().GetBinLowEdge(hist_y_bins) + me.data.GetYaxis().GetBinWidth(hist_y_bins)

                # data should be in the form of data[x][y]
                data = []
                for i in range(1, hist_y_bins + 1):
                    datarow = []
                    for j in range(1, hist_x_bins + 1):
                        datarow.append(me.data.GetBinContent(j, i))
                    data.append(datarow)

                h2d_list.append(
                    dict(
                        title=me.name,
                        entries=entries,
                        data=data,
                        x_min=hist_x_min,
                        x_max=hist_x_max,
                        x_bin=hist_x_bins,
                        y_min=hist_y_min,
                        y_max=hist_y_max,
                        y_bin=hist_y_bins,
                    )
                )

            # print(f'Run #{run} / Lumi #{lumi} / h2d_list len: {len(h2d_list)}')

    def run(self):
        """
        Ingest both H1D and H2D
        """
        self.__h1d()
        self.__h2d()


if __name__ == "__main__":
    import multiprocessing as mp
    import time

    import matplotlib.pyplot as plt
    import psutil

    def target():
        path = "/mnt/dqmio/"
        fpath = f"{path}store_data_Run2022F_ZeroBias_DQMIO_19Jan2023-v2_40000_3A710748-F854-4983-9206-708BAD02F71B.root"
        ing = HistIngestion(fpath)
        ing.run()

    mode = sys.argv[1]

    if mode == "--monitor":
        worker_process = mp.Process(target=target)
        worker_process.start()
        p = psutil.Process(worker_process.pid)

        monitor_log = open(f"monitor-pid-{worker_process.pid}.benchmark-dat", "w")
        monitor_log.write("CPU\tRSS\tVMS\n")

        while worker_process.is_alive():
            cpu = p.cpu_percent()
            rss = p.memory_info().rss / 1024**2
            vms = p.memory_info().vms / 1024**2
            monitor_log.write(f"{cpu}\t{rss}\t{vms}\n")
            time.sleep(0.1)

        worker_process.join()
    elif mode == "--plot":
        pid = sys.argv[2]
        sampling = 10 if len(sys.argv) <= 3 else int(sys.argv[3]) * 10

        with open(f"monitor-pid-{pid}.benchmark-dat", "r") as f:
            lines = f.readlines()

        lines = lines[2:]
        cpu_list = []
        rss_list = []  # physical memory
        # vms_list = [] # virtual memory
        time_list = []
        for idx, line in enumerate(lines):
            cpu, rss, vms = line.split("\t")
            cpu_list.append(float(cpu))
            rss_list.append(float(rss))
            # vms_list.append(float(vms))
            time_list.append(idx)

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("cpu (%)", color="red")
        ax1.plot(time_list[::sampling], cpu_list[::sampling], color="red")

        title = (
            f"sampling: {int(sampling*0.1)} s\n"
            "not considering db interactions\n"
            "store_data_Run2022F_ZeroBias_DQMIO_19Jan2023-v2_40000_3A710748-F854-4983-9206-708BAD02F71B.root (1.5 GB)"
        )
        ax1.set_title(title)

        ax2 = ax1.twinx()
        ax2.set_ylabel("physical memory (MB)", color="blue")
        ax2.plot(time_list[::sampling], rss_list[::sampling], color="blue")

        fig.tight_layout()
        plt.show()
    else:
        quit("Invalid mode.")
