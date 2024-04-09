import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
from PhysioInsight.signal.Plot import eda_res_plot, ecg_res_plot, ppg_res_plot, rsp_res_plot, emg_res_plot
from PhysioInsight.signal.Signal import Signal

from uipy.ui_warn import Warn, Info


class LocalSignal(Signal):
    def __init__(self, local_file, duration):
        self.local_file = local_file
        self.duration = duration
        sampling_rate,name = self.read_local_file()
        super().__init__(duration, sampling_rate, self.signal)
        if name is None:
            self.signal_name = type(self).__name__
        else:
            self.signal_name = name
        self.signal_type = "Unknown"
        self.features = None
        self.classify = False

    def read_local_file(self):
        # 读取txt文件获取numpy数据
        with open(self.local_file, 'r') as file:
            # 读取第一行
            first_line = file.readline().strip()  # 去除换行符和空格
            # 检查第一行是否包含类型信息
            if self.check_type_info(first_line) is not None:
                # 如果包含类型信息，则解析并使用它
                name = first_line
                self.signal_type = first_line
                # 读取剩余行数据
                self.signal=np.loadtxt(file, skiprows=1)
            else:
                # 如果没有类型信息，则直接加载数据
                self.signal = np.loadtxt(self.local_file, dtype=float)
                name=None

        sampling_rate = self.compute_sampling_rate(self.duration)
        return sampling_rate,name
    def check_type_info(self, first_line):
        if first_line in ["ECG", "PPG", "RSP", "EMG","EDA","Unknown"]:
            return first_line
        else:
            return None

    def quick_process(self):
        if self.classify is True:
            self.signal_name=self.signal_type
            self.extract_res=self.local_extract(self.signal_type,self.sampling_rate)
            self.flag[2] = True
            return
        signal, info = self.local_preprocess()
        self.extract_res = self.local_extract(info["Type"], info["sampling_rate"])
        self.signal_type = self.extract_res[1]["Type"]
        self.flag[2] = True
        if self.signal_type == "Unknown":
            self.signal_name = "Unknown"
            Warn("该信号系统判定为Unknown")
            return


    def preprocess(self):
        try:
            self.preprocess_res, self.features = self.local_preprocess()
            self.flag[0] = True
            Info("预处理成功")
        except:
            Warn("预处理失败")

    def extract(self):
        if self.classify is True:
            self.flag[1] = True
            self.extract_res = self.local_extract(self.signal_type, self.sampling_rate)
        else:
            Warn("本地信号需要分类后才能提取特征")

    def easy_classify(self):
        self.signal_type = self.features["Type"]
        self.classify = True
        if self.signal_type == "Unknown":
            self.signal_name = "Unknown"
            Warn("分类为Unknown信号,支持保存此前的预处理结果")
        return self.signal_type

    def local_preprocess(self):
        signal = self.signal
        sampling_rate = self.sampling_rate
        info = {"Type": None}
        duration = len(signal) / sampling_rate
        info["duration"] = duration
        # 标准索引重置
        signal = nk.signal_sanitize(signal)
        info["sampling_rate"] = sampling_rate

        # 获取零点特征
        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        info["ZeroPointsNum"] = len(zero_crossings)

        # 电力线滤波器
        signal = nk.signal_filter(signal, sampling_rate, method='powerline', powerline=40)

        # 计算最大值和最小值的均值
        mean_of_max_min = (np.max(signal) + np.min(signal)) / 2
        info["HalfMean"] = mean_of_max_min


        # 映射图像
        signal = signal_normalize(signal)

        peaks = nk.signal_findpeaks(signal, height_min=0.4)
        info["MorePeaks"] = peaks["Peaks"]
        cleaned_peaks = nk.signal_fixpeaks(peaks, sampling_rate=1000, method='neurokit',
                                           interval_min=0.4,
                                           show=False, robust=True)
        info["Peaks"] = cleaned_peaks[1]

        # 获取周期,利用Peaks
        info["Period"] = compute_period(signal, info["Peaks"], sampling_rate)

        # 利用MorePeaks获取周期
        if info["Period"] is not None:
            info["ZeroPointsNum"] /= (duration / info["Period"])
        else:
            if info["MorePeaks"].shape[0] > 1:
                info["Period"] = compute_period(signal, info["MorePeaks"], sampling_rate)
                info["ZeroPointsNum"] //= (duration / info["Period"])
            else:
                info["Period"] = 0
                info["Rate"] = 0
        # 获取Peaks判别通过的每分钟变化率
        if info["Peaks"].shape[0] > 3:
            info["Rate"] = nk.signal_rate(info["Peaks"], sampling_rate=1000).mean()
        else:
            # 未通过判别暂时为0
            info["Rate"] = 0

        # 初步判断

        if info["ZeroPointsNum"] > 500:
            info["Type"] = 'EMG'
            return signal, info
        if 0 < info["ZeroPointsNum"] < 5 and 0 < info["Rate"] < 160:
            info["Type"] = 'PPG'
            return signal, info
        if info["ZeroPointsNum"] > 10 and 0 < info["Rate"] < 160:
            info["Type"] = 'ECG'
            return signal, info
        T = info["Period"]
        if T != 0:
            info["Rate"] = 60 / T
        # 预处理RSP、EDA
        if info["HalfMean"] > 300:
            info["Type"] = 'RSP'
            return signal, info
        if 10 > info["ZeroPointsNum"] > 0 and info["Period"] > 0 and info["Rate"]<30:
            info["Type"] = 'RSP'
            return signal, info
        # 偏移数据心率重测
        if 30 < info["Rate"] < 161:
            if info["ZeroPointsNum"] > 0:
                info["Type"] = 'ECG'
                return signal, info
            else:
                info["Type"] = 'PPG'
                return signal, info
        if info["ZeroPointsNum"] == 0 and 1 < info["Period"] <= duration and info["HalfMean"]>1:
            info["Type"] = 'EDA'
            return signal, info

        info["Type"] = 'Unknown'
        return signal, info

    def local_extract(self, type, sampling_rate):
        signal = self.signal
        # 初步判断后提取特征，提取失败或提取特征不符合则判断为Unknown
        features = {"Type": None}
        try:
            if type == "ECG":
                signal, features = nk.ecg_process(signal, sampling_rate=sampling_rate)
                features["Type"] = 'ECG'
            elif type == "EDA":
                signal, features = nk.eda_process(signal, sampling_rate=sampling_rate)
                features["Type"] = 'EDA'
            elif type == 'EMG':
                signal, features = nk.emg_process(signal, sampling_rate=sampling_rate)
                features["Type"] = 'EMG'
            elif type == 'PPG':
                signal, features = nk.ppg_process(signal, sampling_rate=sampling_rate)
                features["Type"] = 'PPG'
            elif type == 'RSP':
                signal, features = nk.rsp_process(signal, sampling_rate=sampling_rate)
                features["Type"] = 'RSP'
            else:
                features["Type"] = "Unknown"
        except:
            features["Type"] = 'Unknown'
        return signal, features

    def plot_quick_process_res(self, id):
        try:
            if self.signal_type == "ECG":
                ecg_res_plot(id, self.extract_res[0], self.extract_res[1])
            elif self.signal_type == "EDA":
                eda_res_plot(id,1, self.extract_res[0], self.extract_res[1])
            elif self.signal_type == "PPG":
                ppg_res_plot(id, self.extract_res[0], self.extract_res[1])
            elif self.signal_type == "RSP":
                rsp_res_plot(id,1,self.extract_res[0], self.extract_res[1])
            elif self.signal_type == "EMG":
                emg_res_plot(id, 1,self.extract_res[0], self.extract_res[1])
            plt.show()
        except:
            plt.clf()
            plt.close()
            Warn("信号分类成功:" + self.signal_type + ",但信号失真或过短，无法提取特征")


    def plot_preprocess(self, id):
        self.flag[0] = True
        raw = signal_normalize(self.signal)
        cleand = self.preprocess_res
        nk.signal_plot([raw, cleand], sampling_rate=self.sampling_rate)
        plt.suptitle("LocalSignal Preprocess Result--ID:" + id)
        plt.show()

    def plot_extract(self, id):
        self.plot_quick_process_res(id)

    def compute_sampling_rate(self, duration):
        return len(self.signal) / duration


def signal_normalize(signal):
    max_val = np.max(signal)
    min_val = np.min(signal)
    normalized_signal = (signal - min_val) / (max_val - min_val)
    return normalized_signal


def compute_period(signal, peaks, sampling_rate=1000):
    # 计算峰值之间的距离，即周期
    if len(peaks) > 1:
        period = np.mean(np.diff(peaks)) / sampling_rate
        return period
    elif len(peaks) == 1:
        return len(signal) / sampling_rate
    else:
        return None
