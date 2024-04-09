import gzip
import json

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
from PhysioInsight.uipy.ui_dialog import AddTypeDialog
from PhysioInsight.uipy.ui_warn import Warn, Info
from PyQt5.QtWidgets import QFileDialog, QDialog


class Signal(object):
    def __init__(self, duration, sampling_rate, signal=None):
        self.duration = duration
        self.sampling_rate = sampling_rate
        self.signal = signal
        self.preprocess_res = None
        self.extract_res = None
        self.flag = [False, False, False]  # 0:是否预处理 1:是否提取 2:是否一键处理

    def original_plot(self, id=None):
        nk.signal_plot(self.signal, sampling_rate=self.sampling_rate)
        if id is None:
            plt.title(self.signal_name)
        else:
            plt.title(self.signal_name + "---ID:" + id)
        plt.show()

    def save_as_file(self):
        # 将信号数据保存到文件的方法
        if self.signal is None:
            Warn("没有有效的信号数据用于保存")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getSaveFileName(None, "保存文件", "",
                                                                 "文本文件 (*.txt);;压缩文件 (*.gz)",
                                                                 options=options)
        if file_name:
            # 添加文件后缀名
            file_name_with_extension = self.add_extension(file_name, selected_filter)

            dialog = AddTypeDialog()
            if dialog.exec_() == QDialog.Accepted:
                add_type_info = dialog.is_checked()
            else:
                add_type_info = False
            # 勾选增加信号种类后添加
            signal_name = self.signal_name
            if signal_name=='LocalSignal':
                signal_name = self.signal_type
            # 保存为文本文件或 gzip 压缩文件
            if selected_filter == "文本文件 (*.txt)":
                with open(file_name_with_extension, 'w') as f:
                    # 添加信号种类
                    if add_type_info:
                        f.write(signal_name + '\n')
                    np.savetxt(f, self.signal)
            elif selected_filter == "压缩文件 (*.gz)":
                with gzip.open(file_name_with_extension, 'wt') as f:
                    f.write(signal_name + '\n')
                    np.savetxt(f, self.signal)
            Info("原始信号数据保存成功：" + file_name_with_extension)


    def save_preprocess_as_file(self):
        # 保存预处理后的信号数据到文件的方法
        if self.preprocess_res is None:
            Warn("没有有效的预处理后的信号数据用于保存")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getSaveFileName(None, "保存文件", "",
                                                                 "CSV 文件 (*.csv);;压缩文件 (*.csv.gz)",
                                                                 options=options)
        # 如果用户取消操作，则返回空文件名，不进行保存操作
        if not file_name:
            return

        # 添加文件后缀名
        file_name_with_extension = self.add_extension(file_name, selected_filter)

        # 获取预处理后的信号数据 DataFrame
        preprocessed_df = self.preprocess_res[0]

        # 保存为 CSV 文件或 CSV 压缩过的 gzip 文件
        with open(file_name_with_extension, 'w') as f:
            preprocessed_df.to_csv(f, index=False)
        Info("预处理信号数据保存成功：" + file_name_with_extension)

    def save_features_as_file(self):
        # 保存特征数据到文件的方法
        if self.extract_res is None:
            Warn("没有有效的特征数据用于保存")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getSaveFileName(None, "保存文件", "",
                                                                 "文本文件 (*.txt);;压缩文件 (*.gz)",
                                                                 options=options)
        # 如果用户取消操作，则返回空文件名，不进行保存操作
        if not file_name:
            return

        # 添加文件后缀名
        file_name_with_extension = self.add_extension(file_name, selected_filter)

        # 获取特征数据中的第二个字典
        features_dict = self.extract_res[1]

        # 将字典中的值转换为字符串类型
        features_dict_str = {key: str(value) for key, value in features_dict.items()}

        # 将字典转换成 JSON 格式，并设置换行
        features_json = json.dumps(features_dict_str, indent=4, separators=(',', ': '), ensure_ascii=False)

        # 保存为文本文件或 gzip 压缩文件
        with open(file_name_with_extension, 'w') as f:
            f.write(features_json)
        Info("数据特征保存成功：" + file_name_with_extension)

    def add_extension(self, file_name, selected_filter):
        # 根据选定的文件过滤器添加相应的文件扩展名
        if selected_filter == "文本文件 (*.txt)":
            return file_name + ".txt"
        elif selected_filter == "压缩文件 (*.gz)":
            return file_name + ".gz"
        elif selected_filter == "CSV 文件 (*.csv)":
            return file_name + ".csv"
        elif selected_filter == "压缩文件 (*.csv.gz)":
            return file_name + ".csv.gz"
        else:
            return file_name  # 如果未匹配到任何过滤器，则返回原始文件名

    def get_name(self):
        return self.signal_name
