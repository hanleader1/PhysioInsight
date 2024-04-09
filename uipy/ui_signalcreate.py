from PhysioInsight.uipy.ui_warn import Warn
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QDialog, QMessageBox, QLineEdit


# 输入参数对话框
class ParameterInputDialog(QDialog):
    def __init__(self, parent=None, signal_type=None):
        super().__init__(parent)
        self.signal_type = signal_type
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("输入参数")
        self.layout = QVBoxLayout(self)

        # 创建一个标签和文本框用于输入持续时间
        self.duration_label = QLabel("持续时间 (s)：")
        self.duration_lineedit = QLineEdit()
        if self.signal_type == 'RSP':
            self.duration_lineedit.setText('30')
        else:
            self.duration_lineedit.setText('10')
        self.layout.addWidget(self.duration_label)
        self.layout.addWidget(self.duration_lineedit)

        # 创建一个标签和文本框用于输入采样频率
        self.sampling_rate_label = QLabel("采样频率 (hz)：")
        self.sampling_rate_lineedit = QLineEdit()
        self.sampling_rate_lineedit.setText('250')
        self.layout.addWidget(self.sampling_rate_label)
        self.layout.addWidget(self.sampling_rate_lineedit)

        if self.signal_type == 'ECG' or self.signal_type == 'PPG':
            # 创建一个标签和文本框用于输入心率
            self.heart_rate_label = QLabel("心率 (bpm)：")
            self.heart_rate_lineedit = QLineEdit()
            self.heart_rate_lineedit.setText('70')
            # self.heart_rate_lineedit.setPlaceholderText("默认simple类型")
            self.layout.addWidget(self.heart_rate_label)
            self.layout.addWidget(self.heart_rate_lineedit)
            if self.signal_type == 'ECG':
                self.method_label = QLabel("模拟方式 :")
                self.method_combobox = QComboBox()  # 使用 QComboBox
                self.noise_label = QLabel("模拟噪声:")
                self.noise_lineedit = QLineEdit()
                self.noise_lineedit.setText('0')
                self.method_combobox.addItems(["ecgsyn", "simple"])
                self.layout.addWidget(self.noise_label)
                self.layout.addWidget(self.noise_lineedit)
                self.layout.addWidget(self.method_label)
                self.layout.addWidget(self.method_combobox)
        if self.signal_type == 'EDA':
            self.noise_label = QLabel("模拟噪声:")
            self.noise_lineedit = QLineEdit()
            self.noise_lineedit.setText('0')
            self.scrnum_label = QLabel("皮肤电导反应预期次数:")
            self.scrnum_lineedit = QLineEdit()
            self.scrnum_lineedit.setText('1')
            self.layout.addWidget(self.noise_label)
            self.layout.addWidget(self.noise_lineedit)
            self.layout.addWidget(self.scrnum_label)
            self.layout.addWidget(self.scrnum_lineedit)

        if self.signal_type == 'RSP':
            # 创建一个标签和文本框用于输入呼吸频率
            self.resp_rate_label = QLabel("呼吸频率 ：")
            self.resp_rate_lineedit = QLineEdit()
            self.resp_rate_lineedit.setText('15')
            self.method_label = QLabel("模拟方式 :")
            self.method_combobox = QComboBox()  # 使用 QComboBox
            self.noise_label = QLabel("模拟噪声:")
            self.noise_lineedit = QLineEdit()
            self.noise_lineedit.setText('0')
            self.method_combobox.addItems(["breathmetrics","sinusoidal", "sinus", "simple"])
            self.layout.addWidget(self.resp_rate_label)
            self.layout.addWidget(self.resp_rate_lineedit)
            self.layout.addWidget(self.noise_label)
            self.layout.addWidget(self.noise_lineedit)
            self.layout.addWidget(self.method_label)
            self.layout.addWidget(self.method_combobox)

        if self.signal_type == 'EMG':
            self.noise_label = QLabel("模拟噪声:")
            self.noise_lineedit = QLineEdit()
            self.noise_lineedit.setText('0')
            self.burst_label = QLabel("期望肌肉活跃次数:")
            self.burst_lineedit = QLineEdit()
            self.burst_lineedit.setText('1')
            self.layout.addWidget(self.noise_label)
            self.layout.addWidget(self.noise_lineedit)
            self.layout.addWidget(self.burst_label)
            self.layout.addWidget(self.burst_lineedit)

        if self.signal_type == 'Unknown':
            self.noise_label = QLabel("模拟噪声:")
            self.noise_lineedit = QLineEdit()
            self.noise_lineedit.setText('0')
            self.frequency_label = QLabel("频率(Hz):")
            self.frequency_lineedit = QLineEdit()
            self.frequency_lineedit.setText('10')
            self.amplitude_label = QLabel("振幅:")
            self.amplitude_lineedit = QLineEdit()
            self.amplitude_lineedit.setText('0.5')
            self.layout.addWidget(self.frequency_label)
            self.layout.addWidget(self.frequency_lineedit)
            self.layout.addWidget(self.amplitude_label)
            self.layout.addWidget(self.amplitude_lineedit)
            self.layout.addWidget(self.noise_label)
            self.layout.addWidget(self.noise_lineedit)


        # 创建一个确定按钮和取消按钮
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

    def get_parameters(self):
        try:
            duration = int(self.duration_lineedit.text())
            sampling_rate = int(self.sampling_rate_lineedit.text())
            if self.signal_type == 'RSP' and duration < 10:
                raise ValueError("RSP持续时间必须大于等于10")
            if duration>3600 or duration<1:
                raise ValueError("信号持续时间异常")
            if self.signal_type == 'ECG':
                method = str(self.method_combobox.currentText())
                heart_rate = int(self.heart_rate_lineedit.text())
                noise = float(self.noise_lineedit.text())
                if noise>10 or noise<0:
                    raise ValueError("噪声值异常")
                if heart_rate>180 or heart_rate<5:
                    raise ValueError("心率异常")
                return {'duration': duration, 'heart_rate': heart_rate, 'method': method,
                        'sampling_rate': sampling_rate, 'noise': noise}
            elif self.signal_type == 'RSP':
                resp_rate = int(self.resp_rate_lineedit.text())
                method = str(self.method_combobox.currentText())
                noise = float(self.noise_lineedit.text())
                if noise>10 or noise<0:
                    raise ValueError("噪声值过大")
                return {'duration': duration, 'resp_rate': resp_rate, 'method': method,
                        'noise': noise, 'sampling_rate': sampling_rate}
            elif self.signal_type == 'PPG':
                heart_rate = int(self.heart_rate_lineedit.text())
                return {'duration': duration, 'heart_rate': heart_rate,
                        'sampling_rate': sampling_rate}
            elif self.signal_type == 'EDA':
                scrnum = int(self.scrnum_lineedit.text())
                noise = float(self.noise_lineedit.text())
                return {'duration': duration, 'sampling_rate': sampling_rate,
                        'noise': noise, 'scrnum': scrnum}
            elif self.signal_type == 'EMG':
                noise = float(self.noise_lineedit.text())
                burst = int(self.burst_lineedit.text())
                return {'duration': duration, 'sampling_rate': sampling_rate,
                        'noise': noise, 'burst': burst}
            elif self.signal_type == 'Unknown':
                noise = float(self.noise_lineedit.text())
                frequency = float(self.frequency_lineedit.text())
                amplitude = float(self.amplitude_lineedit.text())
                return {'duration': duration, 'sampling_rate': sampling_rate, 'noise': noise,
                        'frequency': frequency, 'amplitude': amplitude}
        except ValueError as e:
            if e is not None:
                Warn(str(e))
            else:
                QMessageBox.warning(self, "输入错误", "请输入有效的数字")




class SignalTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("选择信号类型")
        self.label = QLabel("请选择要创建的信号类型：")
        self.combobox = QComboBox()
        self.combobox.addItems(
            ["ECG(心电图)", "EDA(皮肤电活动)", "PPG(光电容积脉搏波)", "RSP(呼吸图)", "EMG(肌电信号)",
             "Unknown(未知信号)"])
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.ok_button)

    def get_selected_item(self):
        return self.combobox.currentText().split('(')[0]

