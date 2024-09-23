#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: By 空道
# Created on 10:19 2020/11/12
import os
import sys,re
sys.dont_write_bytecode = True
import logging

# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
from PyQt5 import QtCore, QtGui, QtWidgets
# 导入designer工具生成的login模块
from ui.mainui import Ui_TabWidget
from ui.dialog import Ui_Dialog
from utils.kdsignals import kdSignals
from utils.kdutils import *
import struct

logging.basicConfig(format="%(filename)s %(lineno)s %(funcName)s %(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.FATAL)
g_talbeadd_list = []
g_create_count = 1

class FontNoneDlg(QDialog, Ui_Dialog):
    sendSignal = pyqtSignal(int, str, str)  # 自定义信号

    def __init__(self, parent=None):
        super().__init__(parent)
        # logging.debug(self.parent().windowTitle())
        self.setupUi(self)

        self.pushButton.clicked.connect(self.send)

    def send(self):
        # 发射自定义信号, 并且处理一些格式问题
        ss=self.title_lineEdit.text().strip().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\x00', '')
        kdSignals.send_signals.emit(self.index, ss, self.note_plainTextEdit.toPlainText())

    def setIndex(self, index):
        self.index = index
    def setTitle(self, intitle):
        self.setWindowTitle(intitle)
        return self
class MyMainForm(QTabWidget, Ui_TabWidget):
    def global_init(self):
        self.tabBarDoubleClicked.connect(self.double_clicked)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_change)
        g_talbeadd_list.append(self)
        talbe = QWidget()
        # g_talbeadd.setObjectName("tab_3")
        g_talbeadd_list.append(talbe)
        current_index = self.currentIndex()
        self.insertTab(current_index + 1, talbe, '...')
        self.setCurrentIndex(current_index)

        kdSignals.send_signals.connect(self.dialogUI)
        ##创建一个 非模态对话框;
        self.modalessDialog = FontNoneDlg(self)
    def __init__(self, parent=None):
        global g_talbeadd_list
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.add_left_textEdit.textChanged.connect(self.calc_add_textEdit_changed)
        self.add_right_textEdit.textChanged.connect(self.calc_add_textEdit_changed)
        self.sub_left_textEdit.textChanged.connect(self.calc_sub_textEdit_changed)
        self.sub_right_textEdit.textChanged.connect(self.calc_sub_textEdit_changed)
        self.mul_left_textEdit.textChanged.connect(self.calc_mul_textEdit_changed)
        self.mul_right_textEdit.textChanged.connect(self.calc_mul_textEdit_changed)
        self.div_left_textEdit.textChanged.connect(self.calc_div_textEdit_changed)
        self.div_right_textEdit.textChanged.connect(self.calc_div_textEdit_changed)
        self.xor_left_textEdit.textChanged.connect(self.calc_xor_textEdit_changed)
        self.xor_right_textEdit.textChanged.connect(self.calc_xor_textEdit_changed)
        self.and_left_textEdit.textChanged.connect(self.calc_and_textEdit_changed)
        self.and_right_textEdit.textChanged.connect(self.calc_and_textEdit_changed)
        self.orr_left_textEdit.textChanged.connect(self.calc_orr_textEdit_changed)
        self.orr_right_textEdit.textChanged.connect(self.calc_orr_textEdit_changed)
        self.shl_left_textEdit.textChanged.connect(self.calc_shl_textEdit_changed)
        self.shl_right_textEdit.textChanged.connect(self.calc_shl_textEdit_changed)
        self.shr_left_textEdit.textChanged.connect(self.calc_shr_textEdit_changed)
        self.shr_right_textEdit.textChanged.connect(self.calc_shr_textEdit_changed)
        self.lsl_left_textEdit.textChanged.connect(self.calc_lsl_textEdit_changed)
        self.lsl_right_textEdit.textChanged.connect(self.calc_lsl_textEdit_changed)
        self.ror_left_textEdit.textChanged.connect(self.calc_ror_textEdit_changed)
        self.ror_right_textEdit.textChanged.connect(self.calc_ror_textEdit_changed)
        self.mod_left_textEdit.textChanged.connect(self.calc_mod_textEdit_changed)
        self.mod_right_textEdit.textChanged.connect(self.calc_mod_textEdit_changed)
        self.ord_ord_textEdit.textChanged.connect(self.ord_ord_textEdit_changed)
        self.uord_ord_textEdit.textChanged.connect(self.uord_ord_textEdit_changed)
        self.hex_ord_textEdit.textChanged.connect(self.hex_ord_textEdit_changed)
        self.leb_leb_textEdit.textChanged.connect(self.leb_leb_textEdit_changed)
        self.uleb_leb_textEdit.textChanged.connect(self.uleb_leb_textEdit_changed)
        self.hex_leb_textEdit.textChanged.connect(self.hex_leb_textEdit_changed)
        self.float_float_textEdit.textChanged.connect(self.float_float_textEdit_changed)
        self.double_float_textEdit.textChanged.connect(self.double_float_textEdit_changed)
        self.hex_float_textEdit.textChanged.connect(self.hex_float_textEdit_changed)
        self.left_not_textEdit.textChanged.connect(self.left_not_textEdit_changed)
        self.right_not_textEdit.textChanged.connect(self.right_not_textEdit_changed)

        if 0 == len(g_talbeadd_list):
            self.global_init()
        self.setUsesScrollButtons(True)

    # tab(标签)关闭函数；
    def close_tab(self, index) -> None:
        logging.debug('index:%d' % index)
        if self.count() - 1 != index and (QMessageBox.Yes == QMessageBox.information(self, "title", "是否要关闭[%s]标签" % self.tabText(index), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)):
            self.setCurrentIndex(index - 1)
            g_talbeadd_list.pop(index)
            self.removeTab(index)

    # tab 发生切换
    def tab_change(self, index) -> None:
        global g_create_count
        # ps这个current index  是从左到右依次增加的
        logging.debug('tabchange index:%d' %self.currentIndex())
        if self.count() - 1 == self.currentIndex():
            tab_3 = MyMainForm(self)
            #tab_3.setupUi(self)
            #current_index = self.currentIndex()
            g_talbeadd_list.insert(index, tab_3)
            g_create_count += 1
            self.insertTab(index, tab_3.tab, 'Tab%d'% (g_create_count))
            self.setCurrentIndex(index)

    # double_clicked；
    def double_clicked(self, index) -> None:
        logging.debug('double_clicked:%d' % index)
        tabtitle = self.tabText(index)
        self.modalessDialog.title_lineEdit.setText(tabtitle)
        self.modalessDialog.setIndex(index)
        mynote = g_talbeadd_list[index].line_note.text()
        logging.debug("mynote:" + mynote)
        self.modalessDialog.note_plainTextEdit.setPlainText(mynote)
        self.modalessDialog.setTitle(tabtitle).show()

    def calc_func(self, left_te, right_te, eq_te, operator) -> None:
        left_str = left_te.toPlainText().strip()
        right_str = right_te.toPlainText().strip()
        data = left_str.strip() + right_str.strip()
        if re.match('\A[0-9a-fxA-FX]+\Z', data) is None:
            eq_te.setText("illegal character")
            return
        try:
            if len(left_str) > 0 and len(right_str) > 0:
                leftint = int(left_str, 16)
                rightint = int(right_str, 16)
                armcode = 'int(%d%s%d)' % (leftint, operator, rightint)
                outend = eval(armcode)
                eq_te.setText("0x%x" % (outend & ((1 << 64) - 1)))
        except Exception as e:
            eq_te.setText("illegal character")

    def calc_add_textEdit_changed(self):
        left_str = self.add_left_textEdit.toPlainText()
        right_str = self.add_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.add_left_textEdit, self.add_right_textEdit, self.add_eq_textEdit, '+')
    def calc_sub_textEdit_changed(self):
        left_str = self.sub_left_textEdit.toPlainText()
        right_str = self.sub_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.sub_left_textEdit, self.sub_right_textEdit, self.sub_eq_textEdit, '-')
    def calc_mul_textEdit_changed(self):
        left_str = self.mul_left_textEdit.toPlainText()
        right_str = self.mul_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.mul_left_textEdit, self.mul_right_textEdit, self.mul_eq_textEdit, '*')
    def calc_div_textEdit_changed(self):
        left_str = self.div_left_textEdit.toPlainText()
        right_str = self.div_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.div_left_textEdit, self.div_right_textEdit, self.div_eq_textEdit, '/')
    def calc_xor_textEdit_changed(self):
        left_str = self.xor_left_textEdit.toPlainText()
        right_str = self.xor_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.xor_left_textEdit, self.xor_right_textEdit, self.xor_eq_textEdit, '^')
    def calc_and_textEdit_changed(self):
        left_str = self.and_left_textEdit.toPlainText()
        right_str = self.and_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.and_left_textEdit, self.and_right_textEdit, self.and_eq_textEdit, '&')
    def calc_orr_textEdit_changed(self):
        left_str = self.orr_left_textEdit.toPlainText()
        right_str = self.orr_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.orr_left_textEdit, self.orr_right_textEdit, self.orr_eq_textEdit, '|')
    def calc_shl_textEdit_changed(self):
        left_str = self.shl_left_textEdit.toPlainText()
        right_str = self.shl_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.shl_left_textEdit, self.shl_right_textEdit, self.shl_eq_textEdit, '<<')
    def calc_shr_textEdit_changed(self):
        left_str = self.shr_left_textEdit.toPlainText()
        right_str = self.shr_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.shr_left_textEdit, self.shr_right_textEdit, self.shr_eq_textEdit, '>>')

    def calc_lsl_textEdit_changed(self):
        left_str = self.lsl_left_textEdit.toPlainText().strip()
        right_str = self.lsl_right_textEdit.toPlainText().strip()
        if len(left_str) > 0 and len(right_str) > 0:
            #left_str = left_str.toPlainText().strip()
            #right_str = right_str.toPlainText().strip()
            data = left_str + right_str
            if re.match('\A[0-9a-fxA-FX]+\Z', data) is None:
                self.lsl_eq_textEdit.setText("illegal character")
                return
            try:
                if len(left_str) > 0 and len(right_str) > 0:
                    leftint = int(left_str, 16)
                    rightint = int(right_str, 16)
                    outend = 0
                    if leftint < 0x100000000:
                        outend = ((leftint >> (32 - rightint)) | (leftint << rightint)) & 0xffffffff
                    else:
                        outend = (leftint >> (64 - rightint)) | (leftint << rightint)
                    self.lsl_eq_textEdit.setText("0x%x" % (outend & ((1 << 64) - 1)))
            except Exception as e:
                self.lsl_eq_textEdit.setText("illegal character")
    def calc_ror_textEdit_changed(self):
        left_str = self.ror_left_textEdit.toPlainText().strip()
        right_str = self.ror_right_textEdit.toPlainText().strip()
        if len(left_str) > 0 and len(right_str) > 0:
            # left_str = left_str.toPlainText().strip()
            # right_str = right_str.toPlainText().strip()
            data = left_str + right_str
            if re.match('\A[0-9a-fxA-FX]+\Z', data) is None:
                self.ror_eq_textEdit.setText("illegal character")
                return
            try:
                if len(left_str) > 0 and len(right_str) > 0:
                    leftint = int(left_str, 16)
                    rightint = int(right_str, 16)
                    outend = 0
                    if leftint < 0x100000000:
                        outend = ((leftint << (32 - rightint)) | (leftint >> rightint)) & 0xffffffff
                    else:
                        outend = (leftint << (64 - rightint)) | (leftint >> rightint)
                    self.ror_eq_textEdit.setText("0x%x" % (outend & ((1 << 64) - 1)))
            except Exception as e:
                self.ror_eq_textEdit.setText("illegal character")
    def calc_mod_textEdit_changed(self):
        left_str = self.mod_left_textEdit.toPlainText()
        right_str = self.mod_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.mod_left_textEdit, self.mod_right_textEdit, self.mod_eq_textEdit, '%')

    def ord_ord_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.ord_ord_textEdit.hasFocus():
            ord_ord_str = self.ord_ord_textEdit.toPlainText()
            try:
                if len(ord_ord_str) > 1 or (len(ord_ord_str) == 1 and ord_ord_str[0:1] != '-'):
                    s_hex_neg = struct.pack('l', int(ord_ord_str))
                    self.hex_ord_textEdit.setText(hex(bytes_to_int(s_hex_neg)))
                    self.uord_ord_textEdit.setText("%i" % int.from_bytes(s_hex_neg, byteorder='little', signed=False))
            except Exception as e:
                self.uord_ord_textEdit.setText("illegal character")
                self.hex_ord_textEdit.setText("illegal character")
    def uord_ord_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.uord_ord_textEdit.hasFocus():
            uord_ord_str = self.uord_ord_textEdit.toPlainText()
            try:
                if len(uord_ord_str) > 1 or (len(uord_ord_str) == 1 and uord_ord_str[0:1] != '-'):
                    intval = int(uord_ord_str)
                    s_hex = struct.pack('L', intval)
                    self.hex_ord_textEdit.setText(hex(intval))
                    self.ord_ord_textEdit.setText("%i" % int.from_bytes(s_hex, byteorder='little', signed=True))
            except Exception as e:
                self.ord_ord_textEdit.setText("illegal character")
                self.hex_ord_textEdit.setText("illegal character")
    def hex_ord_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.hex_ord_textEdit.hasFocus():
            hex_ord_str = self.hex_ord_textEdit.toPlainText()
            try:
                if len(hex_ord_str) > 1 or (len(hex_ord_str) == 1 and hex_ord_str[0:1] != '-'):
                    intval = int(hex_ord_str, 16)
                    s_hex = struct.pack('L', intval)
                    self.uord_ord_textEdit.setText("%i" % int.from_bytes(s_hex, byteorder='little', signed=False))
                    self.ord_ord_textEdit.setText("%i" % int.from_bytes(s_hex, byteorder='little', signed=True))
            except Exception as e:
                self.ord_ord_textEdit.setText("illegal character")
                self.uord_ord_textEdit.setText("illegal character")
    def leb_leb_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.leb_leb_textEdit.hasFocus():
            hex_leb_str = self.leb_leb_textEdit.toPlainText().strip().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\x00', '')
            try:
                leb_bytes = hexStringTobytes(hex_leb_str)
                print(leb_bytes)
                intval = leb128_to_int(leb_bytes)
                print(hex(intval))
                s_hex_neg = struct.pack('l', intval)
                uintval = int.from_bytes(s_hex_neg, byteorder='little', signed=False)
                uleb128_bytes = uint_to_uleb128(uintval)
                self.uleb_leb_textEdit.setText(bytesToHexString(uleb128_bytes))
                self.hex_leb_textEdit.setText(hex(uintval))
            except Exception as e:
                self.uleb_leb_textEdit.setText("illegal character")
                self.hex_leb_textEdit.setText("illegal character")
    def uleb_leb_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.uleb_leb_textEdit.hasFocus():
            hex_uleb_str = self.uleb_leb_textEdit.toPlainText().strip().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\x00', '')
            try:
                uleb_bytes = hexStringTobytes(hex_uleb_str)
                print(uleb_bytes)
                uintval = uleb128_to_uint(uleb_bytes)
                s_hex_neg = struct.pack('L', uintval)
                intval = int.from_bytes(s_hex_neg, byteorder='little', signed=True)
                leb128_bytes = int_to_leb128(intval)
                self.leb_leb_textEdit.setText(bytesToHexString(leb128_bytes))
                self.hex_leb_textEdit.setText(hex(intval))
            except Exception as e:
                self.leb_leb_textEdit.setText("illegal character")
                self.hex_leb_textEdit.setText("illegal character")
    def hex_leb_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.hex_leb_textEdit.hasFocus():
            hex_hex_str = self.hex_leb_textEdit.toPlainText().strip().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\x00', '')
            try:
                uintval = int(hex_hex_str,16)
                print(hex(uintval))
                uleb128_bytes = uint_to_uleb128(uintval)
                s_hex_neg = struct.pack('L', uintval)
                intval = int.from_bytes(s_hex_neg, byteorder='little', signed=True)
                leb128_bytes = int_to_leb128(intval)
                self.leb_leb_textEdit.setText(bytesToHexString(leb128_bytes))
                self.uleb_leb_textEdit.setText(bytesToHexString(uleb128_bytes))
            except Exception as e:
                self.leb_leb_textEdit.setText("illegal character")
                self.uleb_leb_textEdit.setText("illegal character")
    def float_float_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.float_float_textEdit.hasFocus():
            float_str = self.float_float_textEdit.toPlainText()
            try:
                floatval = float(float_str)
                print(floatval)
                s_hex_float = struct.pack('f', floatval)
                print(s_hex_float)
                uintval = int.from_bytes(s_hex_float, byteorder='little', signed=False)
                print(hex(uintval))
                s_hex_float = b'\x00\x00\x00\x00' + s_hex_float
                doubleval = struct.unpack('d', s_hex_float)
                self.double_float_textEdit.setText("%.2f" % doubleval)
                self.hex_float_textEdit.setText(hex(uintval))
            except Exception as e:
                self.double_float_textEdit.setText("illegal character")
                self.hex_float_textEdit.setText("illegal character")
    def double_float_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.double_float_textEdit.hasFocus():
            double_str = self.double_float_textEdit.toPlainText()
            try:
                doubleval = float(double_str)
                print(doubleval)
                s_hex_double = struct.pack('d', doubleval)
                #print(s_hex_float)
                uintval = int.from_bytes(s_hex_double, byteorder='little', signed=False)
                print(hex(uintval))
                s_hex_float = s_hex_double[4:8]
                floatval = struct.unpack('f', s_hex_float)
                self.float_float_textEdit.setText("%.2f" % floatval)
                self.hex_float_textEdit.setText(hex(uintval))
            except Exception as e:
                self.float_float_textEdit.setText("illegal character")
                self.hex_float_textEdit.setText("illegal character")
    def hex_float_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.hex_float_textEdit.hasFocus():
            hex_str = self.hex_float_textEdit.toPlainText()
            try:
                longval = int(hex_str, 16)
                s_hex_long = struct.pack('L', longval)
                s_hex_float = s_hex_long[0:4]
                floatval = struct.unpack('f', s_hex_float)
                doubleval = struct.unpack('d', s_hex_long)
                self.float_float_textEdit.setText("%.2f" % floatval)
                self.double_float_textEdit.setText("%.2f" % doubleval)
            except Exception as e:
                self.float_float_textEdit.setText("illegal character")
                self.double_float_textEdit.setText("illegal character")
    def left_not_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.left_not_textEdit.hasFocus():
            hex_str = self.left_not_textEdit.toPlainText()
            try:
                longval = int(hex_str, 16)
                self.right_not_textEdit.setText("0x%x" % (~longval & ((1 << 64) - 1)))
            except Exception as e:
                self.right_not_textEdit.setText("illegal character")
    def right_not_textEdit_changed(self):
        ##判断是否在焦点上来确实是否在输入状态
        if self.right_not_textEdit.hasFocus():
            hex_str = self.right_not_textEdit.toPlainText()
            try:
                longval = int(hex_str, 16)
                self.left_not_textEdit.setText("0x%x" % (~longval & ((1 << 64) - 1)))
            except Exception as e:
                self.left_not_textEdit.setText("illegal character")

    def dialogUI(self, index, intitle, indes):
        logging.debug("index%d, title:%s,des:%s" % (index, intitle, indes))
        self.setTabText(index, intitle)
        g_talbeadd_list[index].line_note.setText(indes)
        self.modalessDialog.close()
if __name__ == '__main__':
    #os.chdir(os.path.dirname(__file__))
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    #myWin.show()
    #mai_dow = QWidget()
    #myWin.setupUi(mai_dow)
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())


