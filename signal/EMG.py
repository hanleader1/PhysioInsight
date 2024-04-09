import neurokit2 as nk
import pandas as pd
from PhysioInsight.signal.Plot import emg_preprocess_plot, emg_res_plot
from PhysioInsight.signal.Signal import Signal
from matplotlib import pyplot as plt
from neurokit2 import signal_sanitize, emg_clean


class EMG(Signal):
    def __init__(self, duration, sampling_rate, noise, burst_number):
        super().__init__(duration, sampling_rate)
        self.noise = noise
        self.burst_number = burst_number
        self.signal = self.generate_signal()
        self.signal_name = type(self).__name__

    def generate_signal(self):
        # 生成 EMG 信号的方法
        return nk.emg_simulate(duration=self.duration, noise=self.noise,
                               sampling_rate=self.sampling_rate, burst_number=self.burst_number)

    def quick_process(self):
        self.flag[2] = True
        self.extract_res = nk.emg_process(self.signal, sampling_rate=self.sampling_rate)

    def preprocess(self):
        self.flag[0] = True
        emg_signal = signal_sanitize(self.signal)
        emg_cleaned = emg_clean(emg_signal, sampling_rate=self.sampling_rate)
        self.preprocess_res = pd.DataFrame({"EMG_Raw": emg_signal, "EMG_Clean": emg_cleaned})

    def extract(self):
        self.flag[1] = True
        self.extract_res = nk.emg_process(self.signal, sampling_rate=self.sampling_rate)

    # 绘制一键处理图像
    def plot_quick_process_res(self, id):
        emg_res_plot(id,1, self.extract_res[0], self.extract_res[1])
        plt.show()

    def plot_preprocess(self, id):
        emg_preprocess_plot(id, self.preprocess_res, self.sampling_rate)
        plt.show()

    def plot_extract(self, id):
        emg_res_plot(id, 0,self.extract_res[0], self.extract_res[1])
        plt.show()
