#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: By 空道
# Created on 10:19 2020/11/12
import os
import sys,re
import time
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
from utils.history import HistoryManager
import struct

logging.basicConfig(format="%(filename)s %(lineno)s %(funcName)s %(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.FATAL)
g_talbeadd_list = []
g_create_count = 1

ERR_PREFIX = "⚠ "
def err(msg): return ERR_PREFIX + msg

ERR_HEX_CHAR    = err("非法 hex 字符")
ERR_DIV_ZERO    = err("除数为 0")
ERR_SHIFT_NEG   = err("位数为负")
ERR_NOT_NUMBER  = err("非数字")
ERR_LEB_HEX     = err("LEB hex 非法")
ERR_LEB_OVER    = err("LEB 长度 > 5 字节")
ERR_FLOAT_BAD   = err("非法浮点数")
ERR_FLOAT_OVER  = err("超出 float32 范围")
ERR_TS_RANGE    = err("超出时间范围")
ERR_DATE_FMT    = err("日期格式错误 (YYYY-MM-DD HH:MM:SS[.fff])")
def err_overflow(width):  return err("超出 %d 位范围" % width)
def err_shift_over(width): return err("位数 ≥ %d" % width)

OP_TABLE = {
    'add':  {'label': '+',    'inputs': ['add_left_textEdit', 'add_right_textEdit'], 'outputs': ['add_eq_textEdit']},
    'sub':  {'label': '-',    'inputs': ['sub_left_textEdit', 'sub_right_textEdit'], 'outputs': ['sub_eq_textEdit']},
    'mul':  {'label': '*',    'inputs': ['mul_left_textEdit', 'mul_right_textEdit'], 'outputs': ['mul_eq_textEdit']},
    'div':  {'label': '/',    'inputs': ['div_left_textEdit', 'div_right_textEdit'], 'outputs': ['div_eq_textEdit']},
    'mod':  {'label': '%',    'inputs': ['mod_left_textEdit', 'mod_right_textEdit'], 'outputs': ['mod_eq_textEdit']},
    'xor':  {'label': '^',    'inputs': ['xor_left_textEdit', 'xor_right_textEdit'], 'outputs': ['xor_eq_textEdit']},
    'and':  {'label': '&',    'inputs': ['and_left_textEdit', 'and_right_textEdit'], 'outputs': ['and_eq_textEdit']},
    'orr':  {'label': '|',    'inputs': ['orr_left_textEdit', 'orr_right_textEdit'], 'outputs': ['orr_eq_textEdit']},
    'shl':  {'label': '<<',   'inputs': ['shl_left_textEdit', 'shl_right_textEdit'], 'outputs': ['shl_eq_textEdit']},
    'shr':  {'label': '>>',   'inputs': ['shr_left_textEdit', 'shr_right_textEdit'], 'outputs': ['shr_eq_textEdit']},
    'lsl':  {'label': '<<<',  'inputs': ['lsl_left_textEdit', 'lsl_right_textEdit'], 'outputs': ['lsl_eq_textEdit']},
    'ror':  {'label': '>>>',  'inputs': ['ror_left_textEdit', 'ror_right_textEdit'], 'outputs': ['ror_eq_textEdit']},
    'ord_from_signed':   {'label': 'signed→hex',   'inputs': ['ord_ord_textEdit'],   'outputs': ['hex_ord_textEdit', 'uord_ord_textEdit']},
    'ord_from_unsigned': {'label': 'unsigned→hex', 'inputs': ['uord_ord_textEdit'],  'outputs': ['hex_ord_textEdit', 'ord_ord_textEdit']},
    'ord_from_hex':      {'label': 'hex→signed',   'inputs': ['hex_ord_textEdit'],   'outputs': ['ord_ord_textEdit', 'uord_ord_textEdit']},
    'leb_from_leb':      {'label': 'leb→hex',      'inputs': ['leb_leb_textEdit'],   'outputs': ['hex_leb_textEdit', 'uleb_leb_textEdit']},
    'leb_from_uleb':     {'label': 'uleb→hex',     'inputs': ['uleb_leb_textEdit'],  'outputs': ['hex_leb_textEdit', 'leb_leb_textEdit']},
    'leb_from_hex':      {'label': 'hex→leb',      'inputs': ['hex_leb_textEdit'],   'outputs': ['leb_leb_textEdit', 'uleb_leb_textEdit']},
    'float_from_float':  {'label': 'float→hex',    'inputs': ['float_float_textEdit'],  'outputs': ['hex_float_textEdit', 'double_float_textEdit']},
    'float_from_double': {'label': 'double→hex',   'inputs': ['double_float_textEdit'], 'outputs': ['hex_float_textEdit', 'float_float_textEdit']},
    'float_from_hex':    {'label': 'hex→float',    'inputs': ['hex_float_textEdit'],    'outputs': ['float_float_textEdit', 'double_float_textEdit']},
    'not_from_left':  {'label': '~left',  'inputs': ['left_not_textEdit'],  'outputs': ['right_not_textEdit']},
    'not_from_right': {'label': '~right', 'inputs': ['right_not_textEdit'], 'outputs': ['left_not_textEdit']},
    'ts_to_date':     {'label': 'ts→date', 'inputs': ['ts_textEdit'],   'outputs': ['date_textEdit']},
    'date_to_ts':     {'label': 'date→ts', 'inputs': ['date_textEdit'], 'outputs': ['ts_textEdit']},
}

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setWindowFlags(Qt.Tool)
        self.resize(420, 480)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget(self)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        self.clear_btn = QPushButton("清空", self)
        self.clear_btn.clicked.connect(self._on_clear)
        self.close_btn = QPushButton("关闭", self)
        self.close_btn.clicked.connect(self.hide)
        btn_row.addStretch(1)
        btn_row.addWidget(self.clear_btn)
        btn_row.addWidget(self.close_btn)
        layout.addLayout(btn_row)

        kdSignals.history_changed.connect(self.refresh)
        self.refresh()

    def refresh(self):
        self.list_widget.clear()
        records = HistoryManager.instance().all()
        for rec in reversed(records):
            label = rec.get('label', rec.get('op', ''))
            inputs = rec.get('inputs', [])
            result = rec.get('result', '')
            if len(inputs) == 1:
                text = "[%s] %s = %s" % (label, inputs[0], result)
            elif len(inputs) >= 2:
                text = "[%s] %s , %s = %s" % (label, inputs[0], inputs[1], result)
            else:
                text = "[%s] = %s" % (label, result)
            item = QListWidgetItem(text)
            ts = rec.get('ts', 0)
            if ts:
                tooltip = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                item.setToolTip(tooltip)
            item.setData(Qt.UserRole, rec)
            self.list_widget.addItem(item)

    def _on_item_double_clicked(self, item):
        rec = item.data(Qt.UserRole)
        if isinstance(rec, dict):
            kdSignals.history_restore.emit(rec)

    def _on_clear(self):
        if QMessageBox.Yes == QMessageBox.question(self, "确认", "确定要清空全部历史记录？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            HistoryManager.instance().clear()
            kdSignals.history_changed.emit()


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

        HistoryManager.instance().load()
        self.history_dialog = HistoryDialog(self)
        self.history_btn = QPushButton("📋 历史", self)
        self.history_btn.setToolTip("查看/恢复历史计算记录")
        self.history_btn.clicked.connect(self._toggle_history_dialog)
        self.setCornerWidget(self.history_btn, Qt.TopRightCorner)
        kdSignals.history_restore.connect(self._on_history_restore)
    def __init__(self, parent=None):
        global g_talbeadd_list
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.bit_width = 64
        self._suppress_history = False
        self._ts_unit = 's'
        self._ts_signal_lock = False
        self.init_bitwidth_ui()
        self.init_timestamp_ui()

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

    def init_bitwidth_ui(self):
        self.bitwidth_group = QtWidgets.QButtonGroup(self.tab)
        self._bitwidth_radios = {
            8: self.bitwidth_radio_8,
            16: self.bitwidth_radio_16,
            32: self.bitwidth_radio_32,
            64: self.bitwidth_radio_64,
        }
        for w, rb in self._bitwidth_radios.items():
            self.bitwidth_group.addButton(rb, w)
            rb.setChecked(w == self.bit_width)
        self.bitwidth_group.idClicked.connect(self._on_bitwidth_changed)

    def init_timestamp_ui(self):
        self.ts_unit_group = QtWidgets.QButtonGroup(self.tab)
        self.ts_unit_group.addButton(self.ts_unit_s_radio, 0)
        self.ts_unit_group.addButton(self.ts_unit_ms_radio, 1)
        self.ts_unit_group.idClicked.connect(self._on_ts_unit_changed)

        self.ts_textEdit.textChanged.connect(self._on_ts_changed)
        self.date_textEdit.textChanged.connect(self._on_date_changed)

        now = int(time.time())
        self._ts_signal_lock = True
        try:
            self.ts_textEdit.setPlainText(str(now))
            self.date_textEdit.setPlainText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
        finally:
            self._ts_signal_lock = False

    def _on_ts_unit_changed(self, btn_id):
        new_unit = 'ms' if btn_id == 1 else 's'
        if new_unit == self._ts_unit:
            return
        self._ts_unit = new_unit
        ts_str = self.ts_textEdit.toPlainText().strip()
        if not ts_str:
            return
        try:
            ts_val = int(ts_str)
        except ValueError:
            return
        if new_unit == 'ms' and ts_val < 10 ** 12:
            new_val = ts_val * 1000
        elif new_unit == 's' and ts_val >= 10 ** 12:
            new_val = ts_val // 1000
        else:
            self._on_ts_changed()
            return
        self._ts_signal_lock = True
        try:
            self.ts_textEdit.setPlainText(str(new_val))
        finally:
            self._ts_signal_lock = False
        self._on_ts_changed()

    def _set_locked(self, widget, text):
        self._ts_signal_lock = True
        try:
            widget.setPlainText(text)
        finally:
            self._ts_signal_lock = False

    def _on_ts_changed(self):
        if self._ts_signal_lock:
            return
        ts_str = self.ts_textEdit.toPlainText().strip()
        if not ts_str:
            self._set_locked(self.date_textEdit, "")
            return
        if not self.ts_textEdit.hasFocus():
            return
        if re.match(r'\A-?\d+\Z', ts_str) is None:
            self._set_locked(self.date_textEdit, ERR_NOT_NUMBER)
            return
        try:
            ts_val = int(ts_str)
            if self._ts_unit == 'ms':
                seconds = ts_val / 1000.0
                ms = ts_val % 1000
                date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds)) + (".%03d" % ms)
            else:
                date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts_val))
        except (OSError, OverflowError, ValueError):
            self._set_locked(self.date_textEdit, ERR_TS_RANGE)
            return
        self._set_locked(self.date_textEdit, date_str)
        self._record_history('ts_to_date', [ts_str, self._ts_unit], date_str)

    def _on_date_changed(self):
        if self._ts_signal_lock:
            return
        date_str = self.date_textEdit.toPlainText().strip()
        if not date_str:
            self._set_locked(self.ts_textEdit, "")
            return
        if not self.date_textEdit.hasFocus():
            return
        ms_part = 0
        date_main = date_str
        if '.' in date_str:
            date_main, frac = date_str.rsplit('.', 1)
            if not frac.isdigit():
                self._set_locked(self.ts_textEdit, ERR_DATE_FMT)
                return
            ms_part = int((frac + '000')[:3])
        try:
            t = time.strptime(date_main, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self._set_locked(self.ts_textEdit, ERR_DATE_FMT)
            return
        try:
            seconds = int(time.mktime(t))
        except (OverflowError, ValueError):
            self._set_locked(self.ts_textEdit, ERR_TS_RANGE)
            return
        if self._ts_unit == 'ms':
            ts_val = seconds * 1000 + ms_part
        else:
            ts_val = seconds
        self._set_locked(self.ts_textEdit, str(ts_val))
        self._record_history('date_to_ts', [date_str, self._ts_unit], str(ts_val))

    def _mask(self):
        return (1 << self.bit_width) - 1

    def _on_bitwidth_changed(self, new_width):
        if new_width == self.bit_width:
            return
        self.bit_width = new_width
        self._recompute_all()

    def _recompute_all(self):
        self._suppress_history = True
        try:
            for op_id, info in OP_TABLE.items():
                first_input_attr = info['inputs'][0]
                widget = getattr(self, first_input_attr, None)
                if widget is None:
                    continue
                if not widget.toPlainText().strip():
                    continue
                slot = self._slot_for_op(op_id)
                if slot is None:
                    continue
                if op_id.startswith(('ord_from', 'leb_from', 'float_from', 'not_from')):
                    widget.setFocus()
                slot()
        finally:
            self._suppress_history = False

    def _slot_for_op(self, op_id):
        mapping = {
            'add': self.calc_add_textEdit_changed,
            'sub': self.calc_sub_textEdit_changed,
            'mul': self.calc_mul_textEdit_changed,
            'div': self.calc_div_textEdit_changed,
            'mod': self.calc_mod_textEdit_changed,
            'xor': self.calc_xor_textEdit_changed,
            'and': self.calc_and_textEdit_changed,
            'orr': self.calc_orr_textEdit_changed,
            'shl': self.calc_shl_textEdit_changed,
            'shr': self.calc_shr_textEdit_changed,
            'lsl': self.calc_lsl_textEdit_changed,
            'ror': self.calc_ror_textEdit_changed,
            'ord_from_signed': self.ord_ord_textEdit_changed,
            'ord_from_unsigned': self.uord_ord_textEdit_changed,
            'ord_from_hex': self.hex_ord_textEdit_changed,
            'leb_from_leb': self.leb_leb_textEdit_changed,
            'leb_from_uleb': self.uleb_leb_textEdit_changed,
            'leb_from_hex': self.hex_leb_textEdit_changed,
            'float_from_float': self.float_float_textEdit_changed,
            'float_from_double': self.double_float_textEdit_changed,
            'float_from_hex': self.hex_float_textEdit_changed,
            'not_from_left': self.left_not_textEdit_changed,
            'not_from_right': self.right_not_textEdit_changed,
        }
        return mapping.get(op_id)

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

    def calc_func(self, left_te, right_te, eq_te, operator, op_id=None) -> None:
        left_str = left_te.toPlainText().strip()
        right_str = right_te.toPlainText().strip()
        if len(left_str) == 0 or len(right_str) == 0:
            return
        if re.match(r'\A[0-9a-fxA-FX]+\Z', left_str + right_str) is None:
            eq_te.setText(ERR_HEX_CHAR)
            return
        try:
            leftint = int(left_str, 16)
            rightint = int(right_str, 16)
        except ValueError:
            eq_te.setText(ERR_HEX_CHAR)
            return
        mask = self._mask()
        leftint &= mask
        rightint &= mask
        if operator in ('/', '%') and rightint == 0:
            eq_te.setText(ERR_DIV_ZERO)
            return
        if operator in ('<<', '>>'):
            if rightint >= self.bit_width:
                eq_te.setText(err_shift_over(self.bit_width))
                return
        try:
            armcode = 'int(%d%s%d)' % (leftint, operator, rightint)
            outend = eval(armcode)
        except Exception:
            eq_te.setText(ERR_HEX_CHAR)
            return
        result = "0x%x" % (outend & mask)
        eq_te.setText(result)
        if op_id is not None:
            self._record_history(op_id, [left_str, right_str], result)

    def calc_add_textEdit_changed(self):
        left_str = self.add_left_textEdit.toPlainText()
        right_str = self.add_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.add_left_textEdit, self.add_right_textEdit, self.add_eq_textEdit, '+', 'add')
    def calc_sub_textEdit_changed(self):
        left_str = self.sub_left_textEdit.toPlainText()
        right_str = self.sub_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.sub_left_textEdit, self.sub_right_textEdit, self.sub_eq_textEdit, '-', 'sub')
    def calc_mul_textEdit_changed(self):
        left_str = self.mul_left_textEdit.toPlainText()
        right_str = self.mul_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.mul_left_textEdit, self.mul_right_textEdit, self.mul_eq_textEdit, '*', 'mul')
    def calc_div_textEdit_changed(self):
        left_str = self.div_left_textEdit.toPlainText()
        right_str = self.div_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.div_left_textEdit, self.div_right_textEdit, self.div_eq_textEdit, '/', 'div')
    def calc_xor_textEdit_changed(self):
        left_str = self.xor_left_textEdit.toPlainText()
        right_str = self.xor_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.xor_left_textEdit, self.xor_right_textEdit, self.xor_eq_textEdit, '^', 'xor')
    def calc_and_textEdit_changed(self):
        left_str = self.and_left_textEdit.toPlainText()
        right_str = self.and_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.and_left_textEdit, self.and_right_textEdit, self.and_eq_textEdit, '&', 'and')
    def calc_orr_textEdit_changed(self):
        left_str = self.orr_left_textEdit.toPlainText()
        right_str = self.orr_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.orr_left_textEdit, self.orr_right_textEdit, self.orr_eq_textEdit, '|', 'orr')
    def calc_shl_textEdit_changed(self):
        left_str = self.shl_left_textEdit.toPlainText()
        right_str = self.shl_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.shl_left_textEdit, self.shl_right_textEdit, self.shl_eq_textEdit, '<<', 'shl')
    def calc_shr_textEdit_changed(self):
        left_str = self.shr_left_textEdit.toPlainText()
        right_str = self.shr_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.shr_left_textEdit, self.shr_right_textEdit, self.shr_eq_textEdit, '>>', 'shr')

    def calc_lsl_textEdit_changed(self):
        self._do_rotate(self.lsl_left_textEdit, self.lsl_right_textEdit, self.lsl_eq_textEdit, 'lsl')
    def calc_ror_textEdit_changed(self):
        self._do_rotate(self.ror_left_textEdit, self.ror_right_textEdit, self.ror_eq_textEdit, 'ror')

    def _do_rotate(self, left_te, right_te, eq_te, op_id):
        left_str = left_te.toPlainText().strip()
        right_str = right_te.toPlainText().strip()
        if len(left_str) == 0 or len(right_str) == 0:
            return
        if re.match(r'\A[0-9a-fxA-FX]+\Z', left_str + right_str) is None:
            eq_te.setText(ERR_HEX_CHAR)
            return
        try:
            leftint = int(left_str, 16)
            n_raw = int(right_str, 16)
        except ValueError:
            eq_te.setText(ERR_HEX_CHAR)
            return
        width = self.bit_width
        mask = self._mask()
        leftint &= mask
        n = n_raw % width
        if n == 0:
            outend = leftint
        elif op_id == 'lsl':
            outend = ((leftint << n) | (leftint >> (width - n))) & mask
        else:
            outend = ((leftint >> n) | (leftint << (width - n))) & mask
        result = "0x%x" % outend
        eq_te.setText(result)
        self._record_history(op_id, [left_str, right_str], result)
    def calc_mod_textEdit_changed(self):
        left_str = self.mod_left_textEdit.toPlainText()
        right_str = self.mod_right_textEdit.toPlainText()
        if len(left_str) > 0 and len(right_str) > 0:
            self.calc_func(self.mod_left_textEdit, self.mod_right_textEdit, self.mod_eq_textEdit, '%', 'mod')

    def ord_ord_textEdit_changed(self):
        if not self.ord_ord_textEdit.hasFocus():
            return
        s = self.ord_ord_textEdit.toPlainText().strip()
        if not s or s == '-':
            return
        if re.match(r'\A-?\d+\Z', s) is None:
            self.uord_ord_textEdit.setText(ERR_NOT_NUMBER)
            self.hex_ord_textEdit.setText(ERR_NOT_NUMBER)
            return
        try:
            intval = int(s)
            s_hex_neg = struct.pack('q', intval)
        except (ValueError, struct.error, OverflowError):
            self.uord_ord_textEdit.setText(err_overflow(64))
            self.hex_ord_textEdit.setText(err_overflow(64))
            return
        hex_result = hex(bytes_to_int(s_hex_neg))
        uord_result = "%i" % int.from_bytes(s_hex_neg, byteorder='little', signed=False)
        self.hex_ord_textEdit.setText(hex_result)
        self.uord_ord_textEdit.setText(uord_result)
        self._record_history('ord_from_signed', [s], hex_result)
    def uord_ord_textEdit_changed(self):
        if not self.uord_ord_textEdit.hasFocus():
            return
        s = self.uord_ord_textEdit.toPlainText().strip()
        if not s:
            return
        if re.match(r'\A\d+\Z', s) is None:
            self.ord_ord_textEdit.setText(ERR_NOT_NUMBER)
            self.hex_ord_textEdit.setText(ERR_NOT_NUMBER)
            return
        try:
            intval = int(s)
            s_hex = struct.pack('Q', intval)
        except (ValueError, struct.error, OverflowError):
            self.ord_ord_textEdit.setText(err_overflow(64))
            self.hex_ord_textEdit.setText(err_overflow(64))
            return
        hex_result = hex(intval)
        ord_result = "%i" % int.from_bytes(s_hex, byteorder='little', signed=True)
        self.hex_ord_textEdit.setText(hex_result)
        self.ord_ord_textEdit.setText(ord_result)
        self._record_history('ord_from_unsigned', [s], hex_result)
    def hex_ord_textEdit_changed(self):
        if not self.hex_ord_textEdit.hasFocus():
            return
        s = self.hex_ord_textEdit.toPlainText().strip()
        if not s:
            return
        s_clean = s[2:] if s.lower().startswith('0x') else s
        if not s_clean or re.match(r'\A[0-9a-fA-F]+\Z', s_clean) is None:
            self.ord_ord_textEdit.setText(ERR_HEX_CHAR)
            self.uord_ord_textEdit.setText(ERR_HEX_CHAR)
            return
        try:
            intval = int(s, 16)
            if intval >= (1 << 64):
                self.ord_ord_textEdit.setText(err_overflow(64))
                self.uord_ord_textEdit.setText(err_overflow(64))
                return
            s_hex = struct.pack('Q', intval)
        except (ValueError, struct.error, OverflowError):
            self.ord_ord_textEdit.setText(err_overflow(64))
            self.uord_ord_textEdit.setText(err_overflow(64))
            return
        uord_result = "%i" % int.from_bytes(s_hex, byteorder='little', signed=False)
        ord_result = "%i" % int.from_bytes(s_hex, byteorder='little', signed=True)
        self.uord_ord_textEdit.setText(uord_result)
        self.ord_ord_textEdit.setText(ord_result)
        self._record_history('ord_from_hex', [s], ord_result)
    def leb_leb_textEdit_changed(self):
        if not self.leb_leb_textEdit.hasFocus():
            return
        raw = self.leb_leb_textEdit.toPlainText().strip()
        hex_leb_str = re.sub(r'\s|\x00', '', raw)
        if not hex_leb_str:
            return
        leb_bytes, perr = self._parse_leb_hex(hex_leb_str)
        if perr:
            self.uleb_leb_textEdit.setText(perr)
            self.hex_leb_textEdit.setText(perr)
            return
        try:
            intval = leb128_to_int(leb_bytes)
            s_hex_neg = struct.pack('q', intval)
            uintval = int.from_bytes(s_hex_neg, byteorder='little', signed=False)
            uleb128_bytes = uint_to_uleb128(uintval)
            hex_result = hex(uintval)
        except Exception:
            self.uleb_leb_textEdit.setText(ERR_LEB_HEX)
            self.hex_leb_textEdit.setText(ERR_LEB_HEX)
            return
        self.uleb_leb_textEdit.setText(bytesToHexString(uleb128_bytes))
        self.hex_leb_textEdit.setText(hex_result)
        self._record_history('leb_from_leb', [hex_leb_str], hex_result)
    def uleb_leb_textEdit_changed(self):
        if not self.uleb_leb_textEdit.hasFocus():
            return
        raw = self.uleb_leb_textEdit.toPlainText().strip()
        hex_uleb_str = re.sub(r'\s|\x00', '', raw)
        if not hex_uleb_str:
            return
        uleb_bytes, perr = self._parse_leb_hex(hex_uleb_str)
        if perr:
            self.leb_leb_textEdit.setText(perr)
            self.hex_leb_textEdit.setText(perr)
            return
        try:
            uintval = uleb128_to_uint(uleb_bytes)
            if uintval == -1:
                raise ValueError
            s_hex_neg = struct.pack('Q', uintval)
            intval = int.from_bytes(s_hex_neg, byteorder='little', signed=True)
            leb128_bytes = int_to_leb128(intval)
            hex_result = hex(intval)
        except Exception:
            self.leb_leb_textEdit.setText(ERR_LEB_HEX)
            self.hex_leb_textEdit.setText(ERR_LEB_HEX)
            return
        self.leb_leb_textEdit.setText(bytesToHexString(leb128_bytes))
        self.hex_leb_textEdit.setText(hex_result)
        self._record_history('leb_from_uleb', [hex_uleb_str], hex_result)
    def hex_leb_textEdit_changed(self):
        if not self.hex_leb_textEdit.hasFocus():
            return
        raw = self.hex_leb_textEdit.toPlainText().strip()
        hex_hex_str = re.sub(r'\s|\x00', '', raw)
        if not hex_hex_str:
            return
        s_clean = hex_hex_str[2:] if hex_hex_str.lower().startswith('0x') else hex_hex_str
        if not s_clean or re.match(r'\A[0-9a-fA-F]+\Z', s_clean) is None:
            self.leb_leb_textEdit.setText(ERR_HEX_CHAR)
            self.uleb_leb_textEdit.setText(ERR_HEX_CHAR)
            return
        try:
            uintval = int(hex_hex_str, 16)
            if uintval >= (1 << 64):
                self.leb_leb_textEdit.setText(err_overflow(64))
                self.uleb_leb_textEdit.setText(err_overflow(64))
                return
            uleb128_bytes = uint_to_uleb128(uintval)
            s_hex_neg = struct.pack('Q', uintval)
            intval = int.from_bytes(s_hex_neg, byteorder='little', signed=True)
            leb128_bytes = int_to_leb128(intval)
            leb_result = bytesToHexString(leb128_bytes)
        except Exception:
            self.leb_leb_textEdit.setText(ERR_HEX_CHAR)
            self.uleb_leb_textEdit.setText(ERR_HEX_CHAR)
            return
        self.leb_leb_textEdit.setText(leb_result)
        self.uleb_leb_textEdit.setText(bytesToHexString(uleb128_bytes))
        self._record_history('leb_from_hex', [hex_hex_str], leb_result)

    @staticmethod
    def _parse_leb_hex(hex_str):
        if re.match(r'\A[0-9a-fA-F]+\Z', hex_str) is None:
            return None, ERR_LEB_HEX
        if len(hex_str) % 2 != 0:
            return None, ERR_LEB_HEX
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            return None, ERR_LEB_HEX
        if len(data) == 0:
            return None, ERR_LEB_HEX
        if len(data) > 5:
            return None, ERR_LEB_OVER
        if (data[-1] & 0x80) != 0:
            return None, err("LEB 未终止")
        return data, None
    def float_float_textEdit_changed(self):
        if not self.float_float_textEdit.hasFocus():
            return
        s = self.float_float_textEdit.toPlainText().strip()
        if not s or s == '-':
            return
        try:
            floatval = float(s)
        except ValueError:
            self.double_float_textEdit.setText(ERR_FLOAT_BAD)
            self.hex_float_textEdit.setText(ERR_FLOAT_BAD)
            return
        FLOAT32_MAX = 3.4028234663852886e+38
        if not (floatval != floatval) and floatval not in (float('inf'), float('-inf')):
            if abs(floatval) > FLOAT32_MAX:
                self.double_float_textEdit.setText(ERR_FLOAT_OVER)
                self.hex_float_textEdit.setText(ERR_FLOAT_OVER)
                return
        try:
            s_hex_float = struct.pack('f', floatval)
        except (OverflowError, struct.error):
            self.double_float_textEdit.setText(ERR_FLOAT_OVER)
            self.hex_float_textEdit.setText(ERR_FLOAT_OVER)
            return
        uintval = int.from_bytes(s_hex_float, byteorder='little', signed=False)
        s_hex_padded = b'\x00\x00\x00\x00' + s_hex_float
        doubleval = struct.unpack('d', s_hex_padded)
        hex_result = hex(uintval)
        self.double_float_textEdit.setText("%.2f" % doubleval)
        self.hex_float_textEdit.setText(hex_result)
        self._record_history('float_from_float', [s], hex_result)
    def double_float_textEdit_changed(self):
        if not self.double_float_textEdit.hasFocus():
            return
        s = self.double_float_textEdit.toPlainText().strip()
        if not s or s == '-':
            return
        try:
            doubleval = float(s)
        except ValueError:
            self.float_float_textEdit.setText(ERR_FLOAT_BAD)
            self.hex_float_textEdit.setText(ERR_FLOAT_BAD)
            return
        try:
            s_hex_double = struct.pack('d', doubleval)
        except (OverflowError, struct.error):
            self.float_float_textEdit.setText(ERR_FLOAT_OVER)
            self.hex_float_textEdit.setText(ERR_FLOAT_OVER)
            return
        uintval = int.from_bytes(s_hex_double, byteorder='little', signed=False)
        s_hex_float = s_hex_double[4:8]
        floatval = struct.unpack('f', s_hex_float)
        hex_result = hex(uintval)
        self.float_float_textEdit.setText("%.2f" % floatval)
        self.hex_float_textEdit.setText(hex_result)
        self._record_history('float_from_double', [s], hex_result)
    def hex_float_textEdit_changed(self):
        if not self.hex_float_textEdit.hasFocus():
            return
        s = self.hex_float_textEdit.toPlainText().strip()
        if not s:
            return
        s_clean = s[2:] if s.lower().startswith('0x') else s
        if not s_clean or re.match(r'\A[0-9a-fA-F]+\Z', s_clean) is None:
            self.float_float_textEdit.setText(ERR_HEX_CHAR)
            self.double_float_textEdit.setText(ERR_HEX_CHAR)
            return
        try:
            longval = int(s, 16)
            if longval >= (1 << 64):
                self.float_float_textEdit.setText(err_overflow(64))
                self.double_float_textEdit.setText(err_overflow(64))
                return
            s_hex_long = struct.pack('Q', longval)
        except (ValueError, struct.error, OverflowError):
            self.float_float_textEdit.setText(err_overflow(64))
            self.double_float_textEdit.setText(err_overflow(64))
            return
        floatval = struct.unpack('f', s_hex_long[0:4])
        doubleval = struct.unpack('d', s_hex_long)
        float_result = "%.2f" % floatval
        self.float_float_textEdit.setText(float_result)
        self.double_float_textEdit.setText("%.2f" % doubleval)
        self._record_history('float_from_hex', [s], float_result)
    def left_not_textEdit_changed(self):
        if self.left_not_textEdit.hasFocus():
            self._do_not(self.left_not_textEdit, self.right_not_textEdit, 'not_from_left')
    def right_not_textEdit_changed(self):
        if self.right_not_textEdit.hasFocus():
            self._do_not(self.right_not_textEdit, self.left_not_textEdit, 'not_from_right')

    def _do_not(self, src_te, dst_te, op_id):
        s = src_te.toPlainText().strip()
        if not s:
            return
        s_clean = s[2:] if s.lower().startswith('0x') else s
        if not s_clean or re.match(r'\A[0-9a-fA-F]+\Z', s_clean) is None:
            dst_te.setText(ERR_HEX_CHAR)
            return
        try:
            mask = self._mask()
            longval = int(s, 16) & mask
        except ValueError:
            dst_te.setText(ERR_HEX_CHAR)
            return
        result = "0x%x" % (~longval & mask)
        dst_te.setText(result)
        self._record_history(op_id, [s], result)

    def _toggle_history_dialog(self):
        if self.history_dialog.isVisible():
            self.history_dialog.hide()
        else:
            self.history_dialog.refresh()
            self.history_dialog.show()
            self.history_dialog.raise_()

    def _record_history(self, op_id, inputs, result, outputs=None):
        if self._suppress_history:
            return
        if op_id not in OP_TABLE:
            return
        if not result or str(result).startswith(ERR_PREFIX) or 'illegal' in str(result):
            return
        cleaned_inputs = [str(x).strip() for x in inputs]
        if any(len(x) == 0 for x in cleaned_inputs):
            return
        HistoryManager.instance().add(op_id, OP_TABLE[op_id]['label'], cleaned_inputs, result, outputs or {})
        kdSignals.history_changed.emit()

    def _on_history_restore(self, record):
        if not g_talbeadd_list or g_talbeadd_list[0] is not self:
            return
        op = record.get('op')
        if op not in OP_TABLE:
            return
        idx = self.currentIndex()
        if idx < 0 or idx >= len(g_talbeadd_list):
            return
        target = g_talbeadd_list[idx]
        if not isinstance(target, MyMainForm):
            return
        input_attrs = OP_TABLE[op]['inputs']
        input_values = record.get('inputs', [])
        if op in ('ts_to_date', 'date_to_ts') and len(input_values) >= 2:
            unit = input_values[1]
            if unit in ('s', 'ms'):
                target._ts_unit = unit
                target.ts_unit_ms_radio.setChecked(unit == 'ms')
                target.ts_unit_s_radio.setChecked(unit == 's')
        for attr, value in zip(input_attrs, input_values):
            widget = getattr(target, attr, None)
            if widget is not None:
                widget.setText(value)
        if input_attrs:
            first = getattr(target, input_attrs[0], None)
            if first is not None:
                first.setFocus()

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
