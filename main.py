import sys

from PhysioInsight.uipy import ui_welcome, ui_mainwindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from uipy.ui_warn import Info


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.ui = ui_welcome.Ui_Welcome()
        self.ui.setupUi(self)
        self.main_window = None
        self.setWindowIcon(QIcon('./icon1.ico'))
        self.ui.start.clicked.connect(self.open_main_window)  # 连接按钮点击事件
        self.ui.textBrowser.verticalScrollBar().valueChanged.connect(self.check_scrollbar_position)  # 连接滚动条位置改变事件

    def open_main_window(self):
        if self.flag is False:
            Info("请阅读完注意事项后使用")
            return
        if self.ui.agree.isChecked():  # 检查是否勾选同意
            self.close()  # 关闭欢迎窗口
            self.main_window = MainWindow()  # 创建主窗口实例
            self.main_window.show()  # 显示主窗口
        else:
            Info("请同意后使用")

    def check_scrollbar_position(self):
        scrollbar = self.ui.textBrowser.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():  # 检查滚动条是否在底部
            self.flag = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_mainwindow.Ui_MainWindow()  # 使用主窗口的UI类
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())
