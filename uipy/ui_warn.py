from PyQt5.QtWidgets import QMessageBox

class Warn(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle("提示")
        self.exec_()

class Info(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle("提示")
        self.exec_()

