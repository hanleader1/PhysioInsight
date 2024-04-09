import io

import neurokit2 as nk
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QSizePolicy, QMainWindow
from matplotlib import pyplot as plt

from uipy.ui_dialog import GetOrder, GetPower, GetNoise, GetRegular, GetOrder1
from uipy.ui_warn import Warn, Info


class Ui_DiyPreprocess(QMainWindow):
    def __init__(self, selected_signal):
        super().__init__()
        self.setWindowTitle("自定义预处理操作")
        self.setWindowIcon(QIcon('./icon1.ico'))
        self.osignal = selected_signal.copy()
        self.diy_signal = selected_signal.copy()
        self.diy_signal.signal = selected_signal.signal.copy()
        self.back_graph = selected_signal.copy()
        self.back_graph.signal=selected_signal.signal.copy()
        print(self.diy_signal)
        self.setupUi(self)
        self.update_show()

    def setupUi(self, DiyPreprocess):
        DiyPreprocess.setObjectName("DiyPreprocess")
        DiyPreprocess.resize(515, 485)
        DiyPreprocess.setMinimumSize(QtCore.QSize(515, 485))
        DiyPreprocess.setMaximumSize(QtCore.QSize(515, 485))
        self.frame = QtWidgets.QFrame(DiyPreprocess)
        self.frame.setGeometry(QtCore.QRect(0, 0, 510, 480))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.filter_method = QtWidgets.QComboBox(self.frame)
        self.filter_method.setGeometry(QtCore.QRect(270, 290, 120, 30))
        self.filter_method.setObjectName("filter_method")
        self.filter_method.addItem("butterworth")
        self.filter_method.addItem("powerline")
        self.filter_method.addItem("bessel")
        self.filter_method.addItem("savgol")
        self.filter_method.addItem("fir")
        self.apply_filter = QtWidgets.QPushButton(self.frame)
        self.apply_filter.setGeometry(QtCore.QRect(400, 290, 100, 30))
        self.apply_filter.setObjectName("apply_filter")
        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 491, 271))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.lowcut = QtWidgets.QDoubleSpinBox(self.frame)
        self.lowcut.setGeometry(QtCore.QRect(50, 290, 70, 28))
        self.lowcut.setObjectName("lowcut")
        self.highcut = QtWidgets.QDoubleSpinBox(self.frame)
        self.highcut.setGeometry(QtCore.QRect(190, 290, 70, 28))
        self.highcut.setObjectName("highcut")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 290, 41, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(150, 290, 41, 30))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(10, 320, 501, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.resample = QtWidgets.QPushButton(self.frame)
        self.resample.setGeometry(QtCore.QRect(190, 340, 71, 30))
        self.resample.setObjectName("resample")
        self.resample_value = QtWidgets.QSpinBox(self.frame)
        self.resample_value.setGeometry(QtCore.QRect(110, 340, 71, 31))
        self.resample_value.setMinimum(10)
        self.resample_value.setMaximum(10000)
        self.resample_value.setProperty("value", 1000)
        self.resample_value.setObjectName("resample_value")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 340, 91, 28))
        self.label_3.setObjectName("label_3")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(10, 370, 501, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setGeometry(QtCore.QRect(260, 328, 20, 50))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.fill_method = QtWidgets.QComboBox(self.frame)
        self.fill_method.setGeometry(QtCore.QRect(280, 340, 111, 30))
        self.fill_method.setObjectName("fill_method")
        self.fill_method.addItem("forward", "forward")
        self.fill_method.addItem("backward", "backward")
        self.fill_method.addItem("both", "both")
        self.fill = QtWidgets.QPushButton(self.frame)
        self.fill.setGeometry(QtCore.QRect(400, 340, 100, 30))
        self.fill.setObjectName("fill")
        self.detrend_method = QtWidgets.QComboBox(self.frame)
        self.detrend_method.setGeometry(QtCore.QRect(280, 390, 111, 30))
        self.detrend_method.setObjectName("detrend_method")
        self.detrend_method.addItem("polynomial")
        self.detrend_method.addItem("tarvainen2002")
        self.detrend_method.addItem("loess")
        self.detrend_method.addItem("locreg")
        self.detrend_method.addItem("emd")
        self.detrend = QtWidgets.QPushButton(self.frame)
        self.detrend.setGeometry(QtCore.QRect(400, 390, 100, 30))
        self.detrend.setObjectName("detrend")
        self.reset = QtWidgets.QPushButton(self.frame)
        self.reset.setGeometry(QtCore.QRect(130, 430, 91, 41))
        self.reset.setObjectName("reset")
        self.back = QtWidgets.QPushButton(self.frame)
        self.back.setGeometry(QtCore.QRect(20, 430, 91, 41))
        self.back.setObjectName("back")
        self.save = QtWidgets.QPushButton(self.frame)
        self.save.setGeometry(QtCore.QRect(370, 430, 131, 41))
        self.save.setObjectName("save")
        self.line_4 = QtWidgets.QFrame(self.frame)
        self.line_4.setGeometry(QtCore.QRect(10, 420, 501, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.frame)
        self.line_5.setGeometry(QtCore.QRect(260, 378, 20, 50))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.noise = QtWidgets.QPushButton(self.frame)
        self.noise.setGeometry(QtCore.QRect(160, 390, 100, 30))
        self.noise.setObjectName("noise")
        self.noise_method = QtWidgets.QComboBox(self.frame)
        self.noise_method.setGeometry(QtCore.QRect(20, 390, 121, 30))
        self.noise_method.setObjectName("noise_method")
        self.noise_method.addItem("laplace","laplace")
        self.noise_method.addItem("gaussian","gaussian")

        # 绑定事件
        self.apply_filter.clicked.connect(self.filter_func)
        self.resample.clicked.connect(self.resample_func)
        self.fill.clicked.connect(self.fill_func)
        self.noise.clicked.connect(self.noise_func)
        self.detrend.clicked.connect(self.detrend_func)
        self.back.clicked.connect(self.back_func)
        self.reset.clicked.connect(self.reset_func)
        self.save.clicked.connect(self.save_func)

        self.retranslateUi(DiyPreprocess)

        self.graphicsView.viewport().installEventFilter(self)

        QtCore.QMetaObject.connectSlotsByName(DiyPreprocess)

    def retranslateUi(self, DiyPreprocess):
        _translate = QtCore.QCoreApplication.translate
        DiyPreprocess.setWindowTitle(_translate("DiyPreprocess", "自定义预处理"))
        self.filter_method.setItemText(0, _translate("DiyPreprocess", "butterworth"))
        self.filter_method.setItemText(1, _translate("DiyPreprocess", "powerline"))
        self.filter_method.setItemText(2, _translate("DiyPreprocess", "bessel"))
        self.filter_method.setItemText(3, _translate("DiyPreprocess", "savgol"))
        self.filter_method.setItemText(4, _translate("DiyPreprocess", "fir"))
        self.apply_filter.setText(_translate("DiyPreprocess", "应用滤波器"))
        self.label.setText(_translate("DiyPreprocess",
                                      "<html><head/><body><p><span style=\" font-size:11pt;\">低通</span></p></body></html>"))
        self.label_2.setText(_translate("DiyPreprocess",
                                        "<html><head/><body><p><span style=\" font-size:11pt;\">高通</span></p></body></html>"))
        self.resample.setText(_translate("DiyPreprocess", "重采样"))
        self.label_3.setText(_translate("DiyPreprocess",
                                        "<html><head/><body><p><span style=\" font-size:11pt;\">重采样频率</span></p></body></html>"))
        self.fill_method.setItemText(0, _translate("DiyPreprocess", "向前填充"))
        self.fill_method.setItemText(1, _translate("DiyPreprocess", "向后填充"))
        self.fill_method.setItemText(2, _translate("DiyPreprocess", "全填充"))
        self.fill.setText(_translate("DiyPreprocess", "重补缺失值"))
        self.detrend_method.setItemText(0, _translate("DiyPreprocess", "polynomial"))
        self.detrend_method.setItemText(1, _translate("DiyPreprocess", "tarvainen2002"))
        self.detrend_method.setItemText(2, _translate("DiyPreprocess", "loess"))
        self.detrend_method.setItemText(3, _translate("DiyPreprocess", "locreg"))
        self.detrend_method.setItemText(4, _translate("DiyPreprocess", "emd"))
        self.detrend.setText(_translate("DiyPreprocess", "信号去趋势"))
        self.reset.setText(_translate("DiyPreprocess", "重置信号"))
        self.back.setText(_translate("DiyPreprocess", "撤销操作"))
        self.save.setText(_translate("DiyPreprocess", "保存预处理结果"))
        self.noise.setText(_translate("DiyPreprocess", "模拟噪声"))
        self.noise_method.setItemText(0, _translate("DiyPreprocess", "拉普拉斯噪声"))
        self.noise_method.setItemText(1, _translate("DiyPreprocess", "高斯噪声"))

    # 展示Signal图像到self.graphicsView = QtWidgets.QGraphicsView(self.frame)
    #         self.graphicsView.setGeometry(QtCore.QRect(10, 10, 491, 271))
    #         self.graphicsView.setObjectName("graphicsView")
    def update_show(self):
        plt.close('all')
        show_signal = self.diy_signal.signal
        scene = QGraphicsScene()

        # 使用 NeuroKit 绘制信号图形
        fig = plt.figure(figsize=(4, 6))  # 指定绘图尺寸
        nk.signal_plot(show_signal, sampling_rate=self.diy_signal.sampling_rate)
        plt.suptitle("Preprocess Result")

        # 将绘制的图形保存为 BytesIO 对象
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # 从 BytesIO 对象创建 QImage 对象
        image = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(image)

        # 创建一个 QGraphicsPixmapItem 对象，并将 QPixmap 添加到场景中
        pixmap_item = QGraphicsPixmapItem(pixmap.scaled(470, 260))
        scene.addItem(pixmap_item)

        plt.close('all')

        # 设置场景
        self.graphicsView.setScene(scene)


    def filter_func(self):
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        lowcut = self.lowcut.value()
        highcut = self.highcut.value()
        method = self.filter_method.currentText()
        print("Applying filter with parameters: lowcut={}, highcut={}, method={}".format(lowcut, highcut, method))
        if highcut == 0:
            highcut = None
        if lowcut == 0:
            lowcut = None
        if method == 'savgol' or method == 'butterworth':
            get = GetOrder()
            if get.exec_():
                order = get.intValue()
                if order is None:
                    return
                if lowcut is None and highcut is None:
                    Warn("你需要给定lowcut或highcut值")
                    return
                self.diy_signal.signal = nk.signal_filter(self.diy_signal.signal,
                                                          sampling_rate=self.diy_signal.sampling_rate, method=method,
                                                          order=order, lowcut=lowcut, highcut=highcut)
                Info("滤波器已使用")
        elif method == 'powerline':
            get = GetPower()
            if get.exec_():
                powerline = get.intValue()
                if powerline is None:
                    return
                self.diy_signal.signal = nk.signal_filter(self.diy_signal.signal,
                                                          sampling_rate=self.diy_signal.sampling_rate,
                                                          method=method, powerline=powerline, lowcut=lowcut,
                                                          highcut=highcut)
                Info("滤波器已使用")
        else:
            self.diy_signal.signal = nk.signal_filter(self.diy_signal.signal,
                                                      sampling_rate=self.diy_signal.sampling_rate, method=method,
                                                      lowcut=lowcut, highcut=highcut)
            Info("滤波器已使用")

        self.update_show()

    def resample_func(self):
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        sampling = self.resample_value.value()
        self.diy_signal.signal = nk.signal_resample(self.diy_signal.signal, sampling_rate=self.diy_signal.sampling_rate,
                                                    desired_sampling_rate=sampling)
        self.diy_signal.sampling_rate = sampling
        Info("重采样成功,当前采样率:" + str(self.diy_signal.sampling_rate))
        self.update_show()

    def fill_func(self):
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        method = self.fill_method.itemData(self.fill_method.currentIndex())
        print(method)
        self.diy_signal.signal = nk.signal_fillmissing(self.diy_signal.signal, method=method)
        Info("填充成功")
        self.update_show()

    def noise_func(self):
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        # 噪声方法  laplace gaussian
        method = self.noise_method.itemData(self.noise_method.currentIndex())
        noise_signal = None
        dialog = GetNoise()
        scale=None
        if dialog.exec_():
            scale = dialog.doubleValue()
            if scale is None:
                return
            if method == "laplace":
                noise_signal = np.random.laplace(loc=0, scale=scale, size=len(self.diy_signal.signal))
                # noise_signal=nk.signal_distort(self.diy_signal.signal,noise_shape="laplace",noise_frequency=scale)
            elif method == "gaussian":
                noise_signal = np.random.normal(loc=0, scale=scale, size=len(self.diy_signal.signal))
        # 将噪声信号添加到原始信号中
        self.diy_signal.signal += noise_signal
        Info("噪声已追加")
        self.update_show()

    def detrend_func(self):
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        method = self.detrend_method.currentText()
        if method == 'polynomial':
            dialog = GetOrder1()
            if dialog.exec_():
                order = dialog.intValue()
                if order is None:
                    return
                self.diy_signal.signal = nk.signal_detrend(self.diy_signal.signal,
                                                           method='polynomial', order=order)
        elif method == 'tarvainen2002':
            dialog = GetRegular()
            if dialog.exec_():
                regular = dialog.intValue()
                if regular is None:
                    return
                self.diy_signal.signal = nk.signal_detrend(self.diy_signal.signal,
                                                           method=method, regularization=regular)
        elif method == 'emd':
            self.diy_signal.signal = nk.signal_detrend(self.diy_signal.signal, method='emd')

        else:
            self.diy_signal.signal = nk.signal_detrend(self.diy_signal.signal,
                                                       sampling_rate=self.diy_signal.sampling_rate,
                                                       method=method)
        Info("去趋势完毕")
        self.update_show()

    def back_func(self):
        if (np.array_equal(self.diy_signal.signal, self.back_graph.signal) and
                self.diy_signal.sampling_rate == self.back_graph.sampling_rate):
            Info("撤销失败")
        else:
            self.diy_signal.signal = self.back_graph.signal.copy()
            self.diy_signal.sampling_rate = self.back_graph.sampling_rate
            self.update_show()
            Info("撤销成功")

    def reset_func(self):
        # 备份
        self.back_graph.signal = self.diy_signal.signal.copy()
        self.back_graph.sampling_rate = self.diy_signal.sampling_rate
        # 恢复为原始
        self.diy_signal.signal = self.osignal.signal.copy()
        self.diy_signal.sampling_rate = self.osignal.sampling_rate

        self.update_show()
        Info("重置成功")

    def save_func(self):
        self.diy_signal.preprocess_res = self.diy_signal.signal
        self.save_preprocess_as_file()
