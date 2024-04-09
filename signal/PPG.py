import neurokit2 as nk
import pandas as pd
from PhysioInsight.signal.Plot import ppg_extract_res_plot, ppg_res_plot, ppg_pre_plot
from PhysioInsight.signal.Signal import Signal
from matplotlib import pyplot as plt
from neurokit2 import as_vector, ppg_methods, ppg_clean, ppg_peaks, signal_rate


class PPG(Signal):
    def __init__(self, duration, heart_rate, sampling_rate):
        super().__init__(duration, sampling_rate)
        self.heart_rate = heart_rate
        self.signal = self.generate_signal()
        self.signal_name = type(self).__name__

    def generate_signal(self):
        # 生成 PPG 信号的方法
        return nk.ppg_simulate(duration=self.duration, heart_rate=self.heart_rate, sampling_rate=self.sampling_rate)


    def preprocess(self):
        sampling_rate=self.sampling_rate
        if self.flag[0] is False:
            self.flag[0] = True
            # Sanitize input
            ppg_signal = as_vector(self.signal)
            methods = ppg_methods(sampling_rate=sampling_rate)
            # Clean signal
            ppg_cleaned = ppg_clean(
                ppg_signal,
                sampling_rate=sampling_rate,
                method=methods["method_cleaning"],
                **methods["kwargs_cleaning"]
            )
            # Find peaks
            peaks_signal, info = ppg_peaks(
                ppg_cleaned,
                sampling_rate=sampling_rate,
                method=methods["method_peaks"],
                **methods["kwargs_peaks"]
            )
            info["sampling_rate"] = sampling_rate  # Add sampling rate in dict info
            # Rate computation
            rate = signal_rate(
                info["PPG_Peaks"], sampling_rate=sampling_rate, desired_length=len(ppg_cleaned)
            )
            # Prepare output
            signals = pd.DataFrame(
                {
                    "PPG_Raw": ppg_signal,
                    "PPG_Clean": ppg_cleaned,
                    "PPG_Rate": rate,
                    "PPG_Peaks": peaks_signal["PPG_Peaks"].values,
                }
            )
            self.preprocess_res = signals, info

    def extract(self):
        self.flag[1] = True
        signals, info = self.preprocess_res
        self.extract_res = [signals, info]

    def quick_process(self):
        self.flag[2] = True
        self.extract_res = nk.ppg_process(self.signal, sampling_rate=self.sampling_rate)

    # 绘制一键处理图像
    def plot_quick_process_res(self, id):
        ppg_res_plot(id, self.extract_res[0], self.extract_res[1])
        plt.show()

    def plot_preprocess(self, id):
        ppg_pre_plot(id, self.preprocess_res[0], self.preprocess_res[1])
        plt.show()

    def plot_extract(self, id):
        ppg_extract_res_plot(id, self.extract_res[0], self.extract_res[1])
        plt.show()

