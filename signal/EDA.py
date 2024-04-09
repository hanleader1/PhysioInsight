import neurokit2 as nk
import pandas as pd
from PhysioInsight.signal.Plot import eda_preprocess_plot, eda_res_plot
from PhysioInsight.signal.Signal import Signal
from matplotlib import pyplot as plt
from neurokit2 import signal_sanitize, eda_clean


class EDA(Signal):
    def __init__(self, duration, sampling_rate, noise, scrnum):
        super().__init__(duration, sampling_rate)
        self.noise = noise
        self.scrnum = scrnum
        self.signal = self.generate_signal()
        self.signal_name = type(self).__name__

    def generate_signal(self):
        # 生成 PPG 信号的方法
        return nk.eda_simulate(duration=self.duration, noise=self.noise, sampling_rate=self.sampling_rate,
                               scr_number=self.scrnum)

    def quick_process(self):
        self.flag[2] = True
        self.extract_res = nk.eda_process(self.signal, sampling_rate=self.sampling_rate)

    def preprocess(self):
        self.flag[0] = True
        eda_signal = signal_sanitize(self.signal)
        eda_cleaned = eda_clean(eda_signal, sampling_rate=self.sampling_rate)
        self.preprocess_res= pd.DataFrame({"EDA_Raw": eda_signal, "EDA_Clean": eda_cleaned})

    def extract(self):
        self.flag[1] = True
        self.extract_res = nk.eda_process(self.signal, sampling_rate=self.sampling_rate)

    # 绘制一键处理图像
    def plot_quick_process_res(self, id):
        eda_res_plot(id, 1,self.extract_res[0], self.extract_res[1])
        plt.show()

    def plot_preprocess(self, id):
        eda_preprocess_plot(id, self.preprocess_res, self.sampling_rate)
        plt.show()

    def plot_extract(self, id):
        eda_res_plot(id,0, self.extract_res[0], self.extract_res[1])
        plt.show()
