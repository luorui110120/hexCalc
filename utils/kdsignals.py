from PyQt5.QtCore import QObject,pyqtSignal
# 自定义信号源对象类型，一定要继承QObject

class kdSignalsCls(QObject):
    #定义一种信号
    data_insert = pyqtSignal(str)
    send_signals = pyqtSignal(int, str, str)  # 自定义信号
    history_restore = pyqtSignal(dict)        # 双击历史项请求恢复输入
    history_changed = pyqtSignal()            # 历史列表发生变化（增/删/清空）

kdSignals = kdSignalsCls()