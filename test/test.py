import neurokit2 as nk
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def signal_normalize(signal):
    max_val = np.max(signal)
    min_val = np.min(signal)
    normalized_signal = (signal - min_val) / (max_val - min_val)
    return normalized_signal


def preprocess(signal, sampling_rate=1000):
    info = {}
    info["Type"]=None
    duration=len(signal) / sampling_rate
    info["duration"] = duration
    # 标准索引重置
    signal = nk.signal_sanitize(signal)
    info["sampling_rate"] = sampling_rate
    # 获取零点特征
    zero_crossings = np.where(np.diff(np.sign(signal)))[0]
    info["ZeroPointsNum"] = len(zero_crossings)
    signal = nk.signal_filter(signal, sampling_rate, method='powerline', powerline=40)
    signal=nk.signal_filter(signal, sampling_rate, method='savgol',window_size=11)
    # 计算最大值和最小值的均值
    mean_of_max_min = (np.max(signal) + np.min(signal)) / 2
    info["HalfMean"] = mean_of_max_min
    # 映射图像
    # signal=nk.signal_detrend(signal,sampling_rate=sampling_rate,method='emd')
    signal = signal_normalize(signal)
    peaks = nk.signal_findpeaks(signal, height_min=0.4)
    info["MorePeaks"] = peaks["Peaks"]
    cleaned_peaks = nk.signal_fixpeaks(peaks, sampling_rate=1000, method='neurokit',
                                       interval_min=0.4,
                                       show=False,robust=True)
    info["Peaks"] = cleaned_peaks[1]
    # 获取周期,利用Peaks
    info["Period"] = compute_period(signal, info["Peaks"], sampling_rate)
    #利用MorePeaks获取周期
    if info["Period"] is not None:
        info["ZeroPointsNum"]/=(duration/info["Period"])
    else:
        if info["MorePeaks"].shape[0] >1:
            info["Period"]=compute_period(signal,info["MorePeaks"],sampling_rate)
            info["ZeroPointsNum"] //= (duration / info["Period"])
        else:
            info["Period"]=0
            info["Rate"] = 0
    # 获取Peaks判别通过的每分钟变化率
    if info["Peaks"].shape[0] > 3:
        info["Rate"] = nk.signal_rate(info["Peaks"], sampling_rate=1000).mean()
    else:
        # 未通过判别暂时为0
        info["Rate"]=0
    # 初步判断
    if info["ZeroPointsNum"]>500:
        info["Type"]='EMG'
        return signal,info
    if 0<info["ZeroPointsNum"]<5 and 0<info["Rate"]<160:
        info["Type"]='PPG'
        return signal,info
    if (info["ZeroPointsNum"]>10 and 0<info["Rate"]<160):
        info["Type"]='ECG'
        return signal,info
    T = info["Period"]
    if T != 0:
        info["Rate"] = 60 / T
    # 预处理RSP、EDA
    if info["HalfMean"]>300:
        info["Type"]='RSP'
        return signal, info
    if 10>info["ZeroPointsNum"]>0 and info["Period"]>0 and info["Rate"]<30:
        info["Type"]='RSP'
        return signal, info
    if 30<info["Rate"]<161:
        if info["ZeroPointsNum"] > 0:
            info["Type"]='ECG'
            return signal, info
        else:
            info["Type"]='PPG'
            return signal, info
    if info["ZeroPointsNum"]==0 and 1<info["Period"]<=duration and info["HalfMean"]>1:
        info["Type"]='EDA'
        return signal, info
    info["Type"]='Unknown'
    return signal,info



def signal_clean(signal, info):
    return signal





def compute_period(signal, peaks, sampling_rate=1000):
    # 计算峰值之间的距离，即周期
    if len(peaks) > 1:
        period = np.mean(np.diff(peaks)) / sampling_rate
        return period
    elif len(peaks) == 1:
        return len(signal) / sampling_rate
    else:
        return None





def extract(signal, info):
    type=info["Type"]
    sampling_rate=info["sampling_rate"]
    # 初步判断后提取特征，提取失败或提取特征不符合则判断为Unknown
    features={}
    try:
        if type=="ECG":
            signal,features=nk.ecg_process(signal, sampling_rate=sampling_rate)
            features["Type"]='ECG'
        elif type=="EDA":
            signal,features=nk.eda_process(signal, sampling_rate=sampling_rate)
            features["Type"]='EDA'
        elif type=='EMG':
            signal, features = nk.eda_process(signal, sampling_rate=sampling_rate)
            features["Type"] = 'EMG'
        elif type=='PPG':
            signal,features=nk.ppg_process(signal, sampling_rate=sampling_rate)
            features["Type"]='PPG'
        elif type=='RSP':
            signal,features=nk.rsp_process(signal, sampling_rate=sampling_rate)
            features["Type"]='RSP'
        else:
            features["Type"]="Unknown"
    except:
        features["Type"]='Unknown'

    return info


def save_features(infos, label, filename):
    # 遍历每个 info，添加 Label 并创建 DataFrame
    dfs = []
    for info in infos:
        info['Label'] = str(label)
        df = pd.DataFrame([info])
        dfs.append(df)

    # 将所有 DataFrame 合并
    df_concat = pd.concat(dfs, ignore_index=True)

    # 检查文件是否存在
    try:
        if pd.read_csv(filename).empty:
            # 如果文件不存在或者文件为空，则直接保存
            df_concat.to_csv(filename, index=False)
        else:
            # 如果文件已存在且不为空，则追加数据
            df_concat.to_csv(filename, mode='a', header=False, index=False)
    except FileNotFoundError:
        # 如果文件不存在，则直接保存
        df_concat.to_csv(filename, index=False)


# ECG模拟simple
# signal_0 = np.loadtxt('E:/code/python code/PhysioInsight/data/unknownSignal/ecg0_10s_1000hz_s.txt', dtype=float)

# ECG模拟带噪声simple
ecg0 = np.loadtxt('./data/unknownSignal/ecg3_360hz_10s_mit.txt')
# ECG生物信号
# data = pd.read_csv("E:/code/python code/PhysioInsight/data/bioData/bio_eventrelated_100hz.csv")
# signal_1 = data["ECG"]

# ECG下载信号
ecg1 = np.loadtxt('./data/unknownSignal/ecg0_10s_1000hz_down.txt')

# EDA模拟噪声
eda0 = np.loadtxt('./data/unknownSignal/eda0_10s_1000hz_noise.txt')

# EDA无噪声
eda1 = np.loadtxt('./data/unknownSignal/eda0_1000hz.txt')

# PPG 模拟信号
ppg0 = np.loadtxt('./data/unknownSignal/ppg_10s_1000hz.txt')
ppg1=np.loadtxt('./data/unknownSignal/ppg_125hz_10s_bidmc.txt')

# EMG模拟带噪声
emg0 = np.loadtxt('./data/unknownSignal/emg1_10s_1000hz_lnoise.txt')

# RSP 下载信号
rsp = np.loadtxt('./data/unknownSignal/rsp0_10s_1000hz_down.txt')

# 自定义RSP信号
rsp1 = np.loadtxt('./data/unknownSignal/rsp0_100s_1000hz_down.txt')
# nk.signal_plot(signal_3, sampling_rate=1000)
# plt.suptitle('Original signal RSP')
# signal1 = preprocess(signal_3)
# nk.signal_plot(signal1, sampling_rate=1000)
# plt.suptitle('Preprocessed RSP')

# unknown
unknown=np.loadtxt('./data/unknownSignal/unknown.txt')


if __name__ == '__main__':
    # nk.signal_plot(signal_0, sampling_rate=1000)
    # plt.suptitle('Original Signal1')
    # nk.signal_plot(signal_1[0:1000], sampling_rate=100)
    # plt.suptitle('Original Signal2')
    ecg0_ = signal_normalize(ecg0)
    preprocessed_ecg0, info0 = preprocess(ecg0,360)
    nk.signal_plot([ecg0_, preprocessed_ecg0], sampling_rate=360)
    info0 = extract(preprocessed_ecg0, info0)
    plt.suptitle("ECG0")

    ecg1_ = signal_normalize(ecg1)
    preprocessed_ecg1, info1 = preprocess(ecg1)
    nk.signal_plot([ecg1_, preprocessed_ecg1], sampling_rate=1000)
    info1 = extract(preprocessed_ecg1, info1)
    plt.suptitle("ECG1")

    ppg_ = signal_normalize(ppg0)
    preprocessed_ppg, info2 = preprocess(ppg0)
    nk.signal_plot([ppg_, preprocessed_ppg], sampling_rate=1000)
    info2 = extract(preprocessed_ppg, info2)
    plt.suptitle("PPG")

    emg_ = signal_normalize(emg0)
    preprocessed_emg, info3 = preprocess(emg0)
    nk.signal_plot([emg_, preprocessed_emg], sampling_rate=1000)
    info3 = extract(preprocessed_emg, info3)
    plt.suptitle("EMG")

    eda_ = signal_normalize(eda0)
    preprocessed_eda, info4 = preprocess(eda0)
    nk.signal_plot([eda_, preprocessed_eda], sampling_rate=1000)
    info4 = extract(preprocessed_eda, info4)
    plt.suptitle("EDA1")

    eda_ = signal_normalize(eda1)
    preprocessed_eda1, info5 = preprocess(eda1)
    nk.signal_plot([eda_, preprocessed_eda1], sampling_rate=1000)
    info5 = extract(preprocessed_eda1, info5)
    plt.suptitle("EDA2")

    rsp_ = signal_normalize(rsp)
    preprocessed_rsp, info6 = preprocess(rsp)
    nk.signal_plot([rsp_, preprocessed_rsp], sampling_rate=1000)
    info6 = extract(preprocessed_rsp, info6)
    plt.suptitle("RSP1")

    rsp_ = signal_normalize(rsp1)
    preprocessed_rsp1, info7 = preprocess(rsp1)
    nk.signal_plot([rsp_, preprocessed_rsp1], sampling_rate=1000)
    info7 = extract(preprocessed_rsp, info7)
    plt.suptitle("RSP2")

    knw_=signal_normalize(unknown)
    preprocessed_knw,info8 = preprocess(knw_)
    info8=extract(preprocessed_knw, info8)

    ppg_=signal_normalize(ppg1)
    preprocessed_ppg,info9 = preprocess(ppg_,sampling_rate=125)
    info9=extract(preprocessed_ppg, info9)

    # 保存特征
    # save_features([info0,info1], 'ECG', './info_data.csv')
    # save_features([info2], 'EMG', './info_data.csv')
    # save_features([info3], 'PPG', './info_data.csv')
    # save_features([info4, info5], 'EDA', './info_data.csv')
    # save_features([info6], 'RSP', './info_data.csv')

    # print("ECG:",info0)
    # print("ECG:",info1)
    # print("PPG:",info2)
    # print("EMG:",info3)

    # print("EDA:",info4)
    # print("EDA:",info5)
    # print("RSP:",info6)

    plt.show()
    print(1)
