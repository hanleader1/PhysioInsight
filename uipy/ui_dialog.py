import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QInputDialog, QCheckBox, QPushButton, QLabel, QVBoxLayout, QDialogButtonBox, \
    QComboBox, QSpinBox, QFileDialog

from uipy.ui_warn import Info


class Local_Duration_Diaglog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.DoubleInput)  # 设置输入模式为小数
        self.setWindowTitle("本地信号持续时间")
        self.setLabelText("输入持续时间(s):")
        self.setDoubleMaximum(3600)  # 设置输入的最大值
        self.setDoubleMinimum(1)  # 设置输入的最小值
        self.setDoubleValue(10)  # 设置默认值


class AddTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("类型追加")
        layout = QVBoxLayout(self)
        self.checkbox = QCheckBox("需要添加信号类型")
        layout.addWidget(self.checkbox)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def is_checked(self):
        return self.checkbox.isChecked()


class DiyChooseDialog(QDialog):
    def __init__(self, diy_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择 DIY 信号ID")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(200)
        # 创建 ComboBox 并添加 DIY 数据中的项
        self.combo_box = QComboBox()
        for key, value in diy_data.items():
            self.combo_box.addItem(str(key), value)

        # 创建按钮，并连接槽函数以处理选择
        select_button = QPushButton("选择ID")
        select_button.clicked.connect(self.accept)

        # 将 ComboBox 和按钮添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(select_button)
        self.setLayout(layout)

    def selected_diy_signal(self):
        # 返回当前选择的 DIY 信号 ID
        return self.combo_box.currentData()


class SignalClassifyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("可选手工分类信号")
        self.label = QLabel("请选择手工分类的信号类型：")
        self.combobox = QComboBox()
        self.combobox.addItems(
            ["ECG(心电图)", "EDA(皮肤电活动)", "PPG(光电容积脉搏波)", "RSP(呼吸图)", "EMG(肌电信号)"])
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.ok_button)

    def get_selected_item(self):
        selected_item = self.combobox.currentText()
        if selected_item == "ECG(心电图)":
            return "ECG"
        elif selected_item == "PPG(光电容积脉搏波)":
            return "PPG"
        elif selected_item == "RSP(呼吸图)":
            return "RSP"
        elif selected_item == "EDA(皮肤电活动)":
            return "EDA"
        elif selected_item == "EMG(肌电信号)":
            return "EMG"
        else:
            return None


class GetOrder(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.IntInput)  # 设置输入模式为小数
        self.setWindowTitle("order值设置")
        self.setLabelText("输入order值(区间2-6):")
        self.setIntMaximum(6)  # 设置输入的最大值
        self.setIntMinimum(2)  # 设置输入的最小值
        self.setIntValue(2)  # 设置默认值

class GetPower(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.IntInput)  # 设置输入模式为小数
        self.setWindowTitle("Powerline设置")
        self.setLabelText("输入值(hz,区间1-100):")
        self.setIntMaximum(100)  # 设置输入的最大值
        self.setIntMinimum(1)  # 设置输入的最小值
        self.setIntValue(50)  # 设置默认值

class GetNoise(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.DoubleInput)  # 设置输入模式为小数
        self.setWindowTitle("模拟噪声标准差")
        self.setLabelText("输入标准差(区间0-10):")
        self.setDoubleMaximum(100)  # 设置输入的最大值
        self.setDoubleMinimum(0)  # 设置输入的最小值
        self.setDoubleValue(1)  # 设置默认值

class GetRegular(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.IntInput)
        self.setWindowTitle("正规化值设置")
        self.setLabelText("输入regular(hz,区间1-2000):")
        self.setIntMaximum(2000)  # 设置输入的最大值
        self.setIntMinimum(1)  # 设置输入的最小值
        self.setIntValue(500)  # 设置默认值

class GetOrder1(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)  # 设置输入窗口的最小宽度
        self.setInputMode(QInputDialog.IntInput)  # 设置输入模式为小数
        self.setWindowTitle("order值设置(0:基线,1:线性,>1:多项式)")
        self.setLabelText("输入order值:")
        self.setIntMaximum(6)  # 设置输入的最大值
        self.setIntMinimum(0)  # 设置输入的最小值
        self.setIntValue(0)  # 设置默认值


class AddClassifyRes(QDialog):
    def __init__(self, signal_type,parent=None,):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("系统分类为:"+signal_type)
        layout = QVBoxLayout(self)
        self.checkbox = QCheckBox("追加系统分类结果到视图")
        layout.addWidget(self.checkbox)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def is_checked(self):
        return self.checkbox.isChecked()

class SplitDataSet(QDialog):
    def __init__(self, parent=None):
        super(SplitDataSet, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('切分数据集(去除N行，N列)')
        self.setMinimumWidth(270)
        self.setMaximumWidth(270)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.file_button = QPushButton('选择数据集文件')
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)
        self.row_spinbox = QSpinBox()
        self.row_spinbox.setRange(0, 100)
        self.row_spinbox.setValue(2)
        self.layout.addWidget(QLabel('切除的行'))
        self.layout.addWidget(self.row_spinbox)
        self.column_spinbox = QSpinBox()
        self.column_spinbox.setRange(0, 100)
        self.column_spinbox.setValue(1)
        self.layout.addWidget(QLabel('切除的列'))
        self.layout.addWidget(self.column_spinbox)
        self.split_button = QPushButton('切分')
        self.split_button.clicked.connect(self.split_dataset)
        self.layout.addWidget(self.split_button)

    def select_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, '选择数据集文件', '', 'Text Files (*.txt);;All Files (*)')
        if self.file_path:
            self.file_button.setText(self.file_path)

    def split_dataset(self):
        if hasattr(self, 'file_path'):
            row=self.row_spinbox.value()
            col=self.column_spinbox.value()
            data = np.genfromtxt(self.file_path, skip_header=row, usecols=(col,))
            save_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', 'Text Files (*.txt);;All Files (*)')
            if save_path:
                np.savetxt(save_path, data)
                Info("保存完毕")