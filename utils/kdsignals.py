from PyQt5.QtCore import QObject,pyqtSignal
# 自定义信号源对象类型，一定要继承QObject

class kdSignalsCls(QObject):
    #定义一种信号
    data_insert = pyqtSignal(str)
    send_signals = pyqtSignal(int, str, str)  # 自定义信号

kdSignals = kdSignalsCls()