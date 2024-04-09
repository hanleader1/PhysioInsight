import time

import neurokit2 as nk
import numpy as np
import pandas as pd
from PhysioInsight.signal.Plot import rsp_res_plot
from PhysioInsight.signal.Signal import Signal
from matplotlib import pyplot as plt
from neurokit2 import rsp_methods, as_vector, rsp_clean


class RSP(Signal):
    def __init__(self, duration, breath_rate, method, noise, sampling_rate):
        super().__init__(duration, sampling_rate)
        self.breath_rate = breath_rate
        self.duration = duration
        self.method = method
        self.noise = noise
        self.signal = self.generate_signal()
        self.signal_name = type(self).__name__

    def generate_signal(self):
        # 生成RSP信号的方法
        seed = int((time.time()) % 2 ** 32)
        # 设置播种种子
        np.random.seed(seed)
        return nk.rsp_simulate(duration=self.duration, method=self.method,
                               respiratory_rate=self.breath_rate, random_state=np.random.RandomState(seed))

    def quick_process(self):
        self.flag[2] = True
        self.extract_res = nk.rsp_process(self.signal, sampling_rate=self.sampling_rate)

    def preprocess(self):
        sampling_rate = self.sampling_rate
        if self.flag[0] is False:
            self.flag[0] = True
            method = "khodadad2018"
            method_rvt = "harrison2021"
            rsp_signal = as_vector(self.signal)
            methods = rsp_methods(
                sampling_rate=sampling_rate, method=method, method_rvt=method_rvt)
            # Clean signal
            rsp_cleaned = rsp_clean(
                rsp_signal,
                sampling_rate=sampling_rate,
                method=methods["method_cleaning"],
                **methods["kwargs_cleaning"],
            )
            # Prepare output
            signals = pd.DataFrame({
                "RSP_Raw": rsp_signal,
                "RSP_Clean": rsp_cleaned,
            }
            )
            self.preprocess_res = signals

    def extract(self):
        self.flag[1] = True
        self.extract_res = nk.rsp_process(self.signal, sampling_rate=self.sampling_rate)

    def plot_quick_process_res(self, id):
        rsp_res_plot(id, 1, self.extract_res[0], self.extract_res[1])
        plt.show()

    def plot_preprocess(self, id):
        nk.signal_plot(self.preprocess_res, sampling_rate=self.sampling_rate)
        plt.suptitle("Respiration(RSP)" + "--ID:" + id + "'s Preprocess Result", fontweight="bold")
        plt.show()

    def plot_extract(self, id):
        rsp_res_plot(id, 0, self.extract_res[0], self.extract_res[1])
        plt.show()
