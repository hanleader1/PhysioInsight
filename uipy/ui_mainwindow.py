import io

import matplotlib.pyplot as plt
import numpy as np
from PhysioInsight.signal.DIY import DIY
from PhysioInsight.signal.ECG import ECG
from PhysioInsight.signal.EDA import EDA
from PhysioInsight.signal.EMG import EMG
from PhysioInsight.signal.LocalSignal import LocalSignal
from PhysioInsight.signal.PPG import PPG
from PhysioInsight.signal.RSP import RSP
from PhysioInsight.signal.Unknown import Unknown
from PhysioInsight.uipy.ui_dialog import Local_Duration_Diaglog, DiyChooseDialog, SignalClassifyDialog, AddClassifyRes, \
    SplitDataSet
from PhysioInsight.uipy.ui_diypreprocess import Ui_DiyPreprocess
from PhysioInsight.uipy.ui_signalcreate import ParameterInputDialog, SignalTypeDialog
from PhysioInsight.uipy.ui_warn import Warn, Info
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QAbstractItemView, QFileDialog, QDialog


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 600)
        MainWindow.setMinimumSize(QtCore.QSize(750, 600))
        MainWindow.setMaximumSize(QtCore.QSize(750, 600))
        MainWindow.setWindowIcon(QIcon('./icon1.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 741, 541))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 26))
        self.menubar.setObjectName("menubar")

        # 创建生理信号
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        # 自定义操作
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.createSignal = QtWidgets.QAction(MainWindow)
        self.createSignal.setObjectName("createSignal")
        self.loadLocal = QtWidgets.QAction(MainWindow)
        self.loadLocal.setObjectName("loadLocal")
        self.customPreprocess = QtWidgets.QAction(MainWindow)
        self.customPreprocess.setObjectName("customPreprocess")

        self.getDataSet=QtWidgets.QAction(MainWindow)
        self.getDataSet.setObjectName("getDataSet")

        self.customAnalysis = QtWidgets.QAction(MainWindow)
        self.customAnalysis.setObjectName("customAnalysis")

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.menu.addAction(self.createSignal)
        self.menu.addAction(self.loadLocal)
        self.menu_2.addAction(self.getDataSet)
        self.menu_2.addAction(self.customPreprocess)
        self.menu_2.addAction(self.customAnalysis)


        # 信号槽连接
        self.createSignal.triggered.connect(self.create_simulation_signal)
        self.loadLocal.triggered.connect(self.load_local_signal)
        self.customPreprocess.triggered.connect(self.custom_preprocess)
        self.customAnalysis.triggered.connect(self.custom_analysis)
        self.getDataSet.triggered.connect(self.get_dataset)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 添加表格
        self.table = QTableWidget(self.frame)
        self.table.setGeometry(QtCore.QRect(10, 10, 740, 540))
        self.table.setObjectName("table")
        self.table.setColumnCount(3)  # 添加三列，分别用于显示ID号、信号名和缩略图
        self.table.setHorizontalHeaderLabels(["ID", "信号类型", "缩略图"])  # 设置列名
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        # 设置ID和信号类型列为不可编辑
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 为表格安装事件过滤器，以捕获鼠标右键事件
        self.table.installEventFilter(self)
        # 用于跟踪信号数据的字典
        self.signal_data = {}
        # diy信号
        self.diy_data = {}
        self.diy_tool = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "生理信号分析平台"))
        self.menu.setTitle(_translate("MainWindow", "创建生理信号"))
        self.menu_2.setTitle(_translate("MainWindow", "自定义操作"))
        self.customPreprocess.setText(_translate("MainWindow", "自定义预处理"))
        self.customAnalysis.setText(_translate("MainWindow", "自定义分析"))
        self.createSignal.setText(_translate("MainWindow", "创建模拟信号"))
        self.loadLocal.setText(_translate("MainWindow", "导入本地信号"))
        self.getDataSet.setText(_translate("MainWindow", "切分数据集"))

    def eventFilter(self, obj, event):
        # 捕获右键操作
        if obj == self.table and event.type() == QEvent.ContextMenu:
            self.show_context_menu(event.globalPos())
            return True
        return super().eventFilter(obj, event)

    # 点击后触发该函数
    def load_local_signal(self):
        # 弹出对话框选择导入文件
        file_name, _ = QFileDialog.getOpenFileName(self)
        if file_name:
            # 弹出对话框让用户输入持续时间
            dialog = Local_Duration_Diaglog()
            ok = dialog.exec_()
            if ok:
                duration = dialog.doubleValue()
                new_signal = LocalSignal(file_name, duration=duration)
                self.show_signal(new_signal)
                self.show_signal_in_table(new_signal)

    def get_dataset(self):
        dialog=SplitDataSet()
        dialog.exec_()


    def show_signal_in_table(self, new_signal):
        # 获取当前行数
        row_count = self.table.rowCount()

        # 添加新行
        self.table.insertRow(row_count)

        max_id = max(self.signal_data.keys()) if self.signal_data else 0
        # 将信号对象添加到字典中
        self.signal_data[max_id + 1] = new_signal

        # 显示ID号
        id_item = QTableWidgetItem(str(max_id+1))
        id_item.setTextAlignment(Qt.AlignCenter)  # 设置内容居中
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)  # 禁止编辑
        self.table.setItem(row_count, 0, id_item)

        # 显示信号名
        signal_name_item = QTableWidgetItem(new_signal.signal_name)
        signal_name_item.setTextAlignment(Qt.AlignCenter)
        signal_name_item.setFlags(signal_name_item.flags() & ~Qt.ItemIsEditable)  # 禁止编辑
        self.table.setItem(row_count, 1, signal_name_item)


        # 显示缩略图
        thumbnail_item = QTableWidgetItem()
        thumbnail_item.setData(Qt.DecorationRole,
                               self.plot_signal_thumbnail(new_signal.signal,new_signal.sampling_rate))
        self.table.setItem(row_count, 2, thumbnail_item)
        self.table.setRowHeight(row_count, 100)

    def show_context_menu(self, pos):
        selected_items = self.table.selectedItems()
        selected_rows = set(item.row() for item in selected_items)
        if not selected_items:  # 没有选中单元格，不显示菜单
            return
        # 创建右键菜单
        menu = QMenu()

        # 添加菜单项
        sub_menu = QMenu("查看缩略图")
        show_original_action = sub_menu.addAction("查看原始信号")
        show_preprocess_action = None
        show_feature_action = None
        for item in selected_items:
            row = item.row()
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)  # 根据信号ID从字典中获取信号对象
            if signal_obj.signal_name != 'Unknown':
                show_preprocess_action = sub_menu.addAction("查看预处理后的信号")
                show_feature_action = sub_menu.addAction("查看提取的特征")
                break
        show_process_action = sub_menu.addAction("查看处理后的信号")
        # 将子菜单添加到主菜单中
        menu.addMenu(sub_menu)
        quick_process_action = menu.addAction("一键处理并提取特征")
        preprocess_action = menu.addAction("预处理")
        sub_menu2 = QMenu("对本地信号分类")

        classify_action = None
        hand_classify_action = None
        for item in selected_items:
            row = item.row()
            signal_id = int(self.table.item(row, 0).text())   # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_obj.signal_name== 'LocalSignal':
                menu.addMenu(sub_menu2)
                classify_action = sub_menu2.addAction("系统分类")
                hand_classify_action = sub_menu2.addAction("手动分类")
                break

        extract_features_action = menu.addAction("提取特征")
        sub_menu1 = QMenu("保存")
        save_action = sub_menu1.addAction("保存原始信号到本地")
        # 如果信号提取过特征，则显示保存特征到本地的选项
        save_features_action = None
        save_preprocess_action = None
        for item in selected_items:
            row = item.row()
            signal_id = int(self.table.item(row, 0).text())   # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_obj.flag[0]:
                save_preprocess_action = sub_menu1.addAction("保存预处理数据到本地")
            if signal_obj.flag[1] or signal_obj.flag[2]:
                save_features_action = sub_menu1.addAction("保存信号特征到本地")
                break

        menu.addMenu(sub_menu1)
        delete_action = menu.addAction("删除信号")
        # 连接菜单项的信号和槽
        delete_action.triggered.connect(lambda: self.delete_selected_signals(selected_rows))
        quick_process_action.triggered.connect(lambda: self.quick_process_selected_signals(selected_rows))
        preprocess_action.triggered.connect(lambda: self.preprocess_selected_signals(selected_rows))
        extract_features_action.triggered.connect(lambda: self.extract_features_selected_signals(selected_rows))
        save_action.triggered.connect(lambda: self.save_selected_signals(selected_rows))
        if hand_classify_action:
            hand_classify_action.triggered.connect(lambda: self.hand_classify_selected_signals(selected_rows))
        if classify_action:
            classify_action.triggered.connect(lambda: self.classify_selected_signals(selected_rows))
        if save_features_action:
            save_features_action.triggered.connect(lambda: self.save_features_selected_signals(selected_rows))
        if save_preprocess_action:
            save_preprocess_action.triggered.connect(lambda: self.save_preprocess_selected_signals(selected_rows))
        show_original_action.triggered.connect(lambda: self.show_img(selected_items, 1))
        if show_preprocess_action:
            show_preprocess_action.triggered.connect(lambda: self.show_img(selected_items, 2))
        if show_feature_action:
            show_feature_action.triggered.connect(lambda: self.show_img(selected_items, 3))

        show_process_action.triggered.connect(lambda: self.show_img(selected_items, 4))

        menu.exec_(pos)

    def show_img(self, rows, signal_type):
        # 展示该信号图片
        for item in rows:
            row = item.row()
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_obj:
                if signal_type == 1:
                    # 展示原始信号图片
                    signal_obj.original_plot(str(signal_id))
                elif signal_type == 2:
                    # 展示预处理后的信号图片
                    if signal_obj.flag[0] is True:
                        signal_obj.plot_preprocess(str(signal_id))
                    else:
                        Warn("还未经预处理")
                elif signal_type == 3:
                    # 展示提取特征后的图片
                    if signal_obj.flag[1] or signal_obj.flag[2] is True:
                        signal_obj.plot_extract(str(signal_id))
                    else:
                        Warn("还未提取特征")
                else:
                    # 展示一键处理后的图片
                    if signal_obj.flag[2] or signal_obj.flag[1]:
                        if signal_obj.signal_name == 'Unknown':
                            Warn("Unknown信号未经处理")
                            return
                        signal_obj.plot_quick_process_res(str(signal_id))
                    else:
                        Warn("还未一键处理")

    def delete_selected_signals(self, rows):
        rows_to_delete = sorted(rows, reverse=True)
        for row in rows_to_delete:
            if row < 0 or row >= self.table.rowCount():  # 行号不合法，直接跳过
                continue
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            self.table.removeRow(row)
            # 删除与该行相关的信号对象
            if signal_id in self.signal_data:
                del self.signal_data[signal_id]

    def save_features_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text()) # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                signal_obj.save_features_as_file()

    def save_preprocess_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                signal_obj.save_preprocess_as_file()

    def preprocess_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():  # 行号不合法，直接跳过
                continue
            signal_id = int(self.table.item(row, 0).text())# 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                if signal_obj.signal_name == 'Unknown':
                    Warn("该信号暂无预处理操作")
                    return
                if signal_obj.flag[0] is False:
                    signal_obj.preprocess()
                    signal_obj.plot_preprocess(str(signal_id))
                else:
                    Warn("信号已经预处理过")

    def extract_features_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                if hasattr(signal_obj, 'signal_type') and signal_obj.signal_type is not None:
                    if signal_obj.signal_type == 'Unknown':
                        Warn("未知信号无法提取特征")
                        return
                if signal_obj.flag[1] is False:
                    if signal_obj.flag[0]:
                        signal_obj.extract()
                        if (signal_obj.signal_name == 'LocalSignal' and
                                signal_obj.classify is False):
                            return
                        signal_obj.plot_extract(str(signal_id))
                    else:
                        Warn("信号还未经预处理")
                else:
                    Warn("信号已经提取过特征")

    def quick_process_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text()) # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                if signal_obj.signal_name == 'Unknown':
                    Warn("Unknown信号无处理操作")
                    return
                if signal_obj.flag[2] is False:
                    signal_obj.quick_process()
                    if signal_obj == 'Unknown':
                        Warn("经判断为Unknown信号，其无处理操作")
                        return
                    signal_obj.plot_quick_process_res(str(signal_id))
                    if signal_obj.signal_name == 'LocalSignal':
                        print("这是" + signal_obj.signal_type + "信号")
                        # 是否更新信号
                else:
                    Warn("信号已经处理过并提取特征")

    def classify_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                if signal_obj.flag[0] is True:
                    signal_type=signal_obj.easy_classify()
                    dialog = AddClassifyRes(signal_type)
                    if dialog.exec_() == QDialog.Accepted:
                        add_type_info = dialog.is_checked()
                    else:
                        add_type_info = False
                    if add_type_info:
                        # 追加信号类型到选中行的第1列文字后
                        current_text = self.table.item(row, 1).text()  # 获取选中行的文本内容
                        new_text = current_text + "(" + signal_type + ")"  # 在文本内容后面追加信号类型
                        self.table.item(row, 1).setText(new_text)  # 将更新后的文本内容设置回选中行的第1列
                else:
                    Warn("系统自动分类前需要先预处理")

    def hand_classify_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text())  # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                dialog = SignalClassifyDialog(self)
                if dialog.exec_():
                    signal_type = dialog.get_selected_item()
                    if signal_type is not None:
                        signal_obj.signal_type = signal_type
                        signal_obj.classify = True
                        dialog = AddClassifyRes(signal_type)
                        if dialog.exec_() == QDialog.Accepted:
                            add_type_info = dialog.is_checked()
                        else:
                            add_type_info = False
                        if add_type_info:
                            # 追加信号类型到选中行的第1列文字后
                            current_text = self.table.item(row, 1).text()  # 获取选中行的文本内容
                            new_text = current_text + "(" + signal_type + ")"  # 在文本内容后面追加信号类型
                            self.table.item(row, 1).setText(new_text)  # 将更新后的文本内容设置回选中行的第1列
                    else:
                        Warn("未选择信号")

    def save_selected_signals(self, rows):
        for row in rows:
            if row < 0 or row >= self.table.rowCount():
                continue
            signal_id = int(self.table.item(row, 0).text()) # 获取信号ID
            signal_obj = self.signal_data.get(signal_id)
            if signal_id in self.signal_data:
                signal_obj.save_as_file()

    def create_simulation_signal(self):
        dialog = SignalTypeDialog(self)
        if dialog.exec_():
            signal_type = dialog.get_selected_item()
            parameters = self.get_signal_parameters(signal_type)
            if parameters:
                new_signal = self.generate_signal(signal_type, parameters)
                self.show_signal(new_signal)
                self.show_signal_in_table(new_signal)

    def plot_signal_thumbnail(self, signal,sampling_rate):
        # 创建缩略图并将其转换为QPixmap
        plt.figure(figsize=(4.3, 1.25))  # 设置缩略图的高度与单元格的高度成比例
        time = np.arange(len(signal)) / sampling_rate
        plt.plot(time,signal)
        plt.tight_layout()
        # 将图像保存到内存中
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        # 从内存加载图像
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        # 清除图形以释放内存
        plt.close()
        return pixmap

    # 生成信号
    def generate_signal(self, signal_type, parameters):
        new_signal = None
        if signal_type == 'ECG':
            new_signal = ECG(duration=parameters['duration'], heart_rate=parameters['heart_rate'],
                             method=parameters['method'], sampling_rate=parameters['sampling_rate'],
                             noise=parameters['noise'])
        elif signal_type == 'PPG':
            new_signal = PPG(duration=parameters['duration'], heart_rate=parameters['heart_rate'],
                             sampling_rate=parameters['sampling_rate'])
        elif signal_type == 'RSP':
            new_signal = RSP(duration=parameters['duration'], breath_rate=parameters['resp_rate'],
                             sampling_rate=parameters['sampling_rate']
                             , method=parameters['method'], noise=parameters['noise'])
        elif signal_type == 'EDA':
            new_signal = EDA(duration=parameters['duration'], noise=parameters['noise'],
                             sampling_rate=parameters['sampling_rate'], scrnum=parameters['scrnum'])
        elif signal_type == 'EMG':
            new_signal = EMG(duration=parameters['duration'], noise=parameters['noise'],
                             sampling_rate=parameters['sampling_rate'], burst_number=parameters['burst'])
        elif signal_type == 'Unknown':
            new_signal = Unknown(duration=parameters['duration'], sampling_rate=parameters['sampling_rate'],
                                 noise=parameters['noise'], frequency=parameters['frequency'],
                                 amplitude=parameters['amplitude'])
        return new_signal

    def show_signal(self, new_signal):
        new_signal.original_plot()

    # 获取创建信号参数
    def get_signal_parameters(self, signal_type):
        dialog = ParameterInputDialog(self, signal_type=signal_type)
        if dialog.exec_():
            return dialog.get_parameters()
        else:
            return None

    def custom_preprocess(self):
        # 遍历data中的LocalSignal
        for key, value in self.signal_data.items():
            if isinstance(value, LocalSignal):
                # 创建 DIY 对象并将 LocalSignal 的信号赋值给它
                diy_signal = DIY(value.signal, value.duration, value.sampling_rate)
                # 将 DIY 对象添加到信号数据的字典中
                self.diy_data[key] = diy_signal
        # 没有LocalSignal
        if len(self.diy_data) == 0:
            Info("需要先导入本地信号")
            return
        # 调用选择当前可以diy的id号窗口
        dialog = DiyChooseDialog(self.diy_data)
        selected_signal = None
        if dialog.exec_() == QDialog.Accepted:
            selected_signal = dialog.selected_diy_signal()
            print("选择的 DIY 信号:", selected_signal)
            # 传入选中的信号对象
            self.diy_tool = Ui_DiyPreprocess(selected_signal)
            self.diy_tool.show()

    def custom_analysis(self):
        Info("功能正在开发中")
        return
