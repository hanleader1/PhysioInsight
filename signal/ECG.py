import neurokit2 as nk
import pandas as pd
from PhysioInsight.signal.Plot import ecg_res_plot, ecg_extract_res_plot, ecg_pre_plot
from PhysioInsight.signal.Signal import Signal
from matplotlib import pyplot as plt
from neurokit2 import ecg_delineate, ecg_phase, signal_sanitize


class ECG(Signal):
    def __init__(self, duration, heart_rate, method, sampling_rate, noise=0.0):
        super().__init__(duration, sampling_rate)
        self.heart_rate = heart_rate
        self.method = method
        self.noise = noise
        self.signal = self.generate_signal()
        self.signal_name = type(self).__name__

    def generate_signal(self):
        # 生成 ECG 信号的方法
        return nk.ecg_simulate(duration=self.duration, heart_rate=self.heart_rate, method=self.method,
                               sampling_rate=self.sampling_rate,noise=self.noise)

    def quick_process(self):
        self.flag[2] = True
        self.extract_res = nk.ecg_process(self.signal, sampling_rate=self.sampling_rate)

    def preprocess(self):
        sampling_rate=self.sampling_rate
        if self.flag[0] is False:
            self.flag[0] = True
            ecg_signal = signal_sanitize(self.signal)
            ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate)
            instant_peaks, info = nk.ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate, correct_artifacts=True, )
            rate = nk.ecg_rate(info, sampling_rate=sampling_rate, desired_length=len(ecg_cleaned))
            quality = nk.ecg_quality(ecg_cleaned, rpeaks=info["ECG_R_Peaks"], sampling_rate=sampling_rate)
            signals = pd.DataFrame({"ECG_Raw": self.signal,
                                    "ECG_Clean": ecg_cleaned,
                                    "ECG_Rate": rate,
                                    "ECG_Quality": quality})
            signals = pd.concat([signals, instant_peaks], axis=1)
            # Create info dict
            info["sampling_rate"] = sampling_rate
            self.preprocess_res = signals, info

    def extract(self):
        self.flag[1] = True
        # Delineate QRS complex
        signals, info = self.preprocess_res
        self.extract_res = [signals, info]
        delineate_signal, delineate_info = ecg_delineate(
            ecg_cleaned=signals["ECG_Clean"], rpeaks=info["ECG_R_Peaks"], sampling_rate=info["sampling_rate"]
        )
        # info 追加R峰
        self.extract_res[1].update(delineate_info)  # Merge waves indices dict with info dict

        # Determine cardiac phases
        cardiac_phase = ecg_phase(
            ecg_cleaned=signals["ECG_Clean"],
            rpeaks=info["ECG_R_Peaks"],
            delineate_info=delineate_info,
        )

        # Add additional information to signals DataFrame
        self.extract_res[0] = pd.concat(
            [signals, signals["ECG_R_Peaks"], delineate_signal, cardiac_phase], axis=1
        )

    # 绘制一键处理图像
    def plot_quick_process_res(self, id):
        ecg_res_plot(id, self.extract_res[0], self.extract_res[1])
        plt.show()

    # 绘制预处理的图像
    def plot_preprocess(self, id):
        ecg_pre_plot(id,self.preprocess_res[0], self.preprocess_res[1])
        plt.show()

    def plot_extract(self, id):
        ecg_extract_res_plot(id, self.extract_res[0], self.extract_res[1])
        plt.show()
