# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(775, 712)
        TabWidget.setTabsClosable(True)
        TabWidget.setMovable(True)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.add_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.add_eq_textEdit.setGeometry(QtCore.QRect(530, 20, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_eq_textEdit.setFont(font)
        self.add_eq_textEdit.setReadOnly(True)
        self.add_eq_textEdit.setAcceptRichText(False)
        self.add_eq_textEdit.setObjectName("add_eq_textEdit")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(250, 20, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.add_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.add_right_textEdit.setGeometry(QtCore.QRect(300, 20, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_right_textEdit.setFont(font)
        self.add_right_textEdit.setAcceptRichText(False)
        self.add_right_textEdit.setObjectName("add_right_textEdit")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(500, 20, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.add_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.add_left_textEdit.setGeometry(QtCore.QRect(50, 20, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_left_textEdit.setFont(font)
        self.add_left_textEdit.setAcceptRichText(False)
        self.add_left_textEdit.setObjectName("add_left_textEdit")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(250, 70, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.sub_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.sub_eq_textEdit.setGeometry(QtCore.QRect(530, 70, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sub_eq_textEdit.setFont(font)
        self.sub_eq_textEdit.setReadOnly(True)
        self.sub_eq_textEdit.setAcceptRichText(False)
        self.sub_eq_textEdit.setObjectName("sub_eq_textEdit")
        self.sub_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.sub_left_textEdit.setGeometry(QtCore.QRect(50, 70, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sub_left_textEdit.setFont(font)
        self.sub_left_textEdit.setAcceptRichText(False)
        self.sub_left_textEdit.setObjectName("sub_left_textEdit")
        self.sub_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.sub_right_textEdit.setGeometry(QtCore.QRect(300, 70, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sub_right_textEdit.setFont(font)
        self.sub_right_textEdit.setAcceptRichText(False)
        self.sub_right_textEdit.setObjectName("sub_right_textEdit")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(500, 70, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(250, 130, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.mul_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mul_eq_textEdit.setGeometry(QtCore.QRect(530, 120, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mul_eq_textEdit.setFont(font)
        self.mul_eq_textEdit.setReadOnly(True)
        self.mul_eq_textEdit.setAcceptRichText(False)
        self.mul_eq_textEdit.setObjectName("mul_eq_textEdit")
        self.mul_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mul_left_textEdit.setGeometry(QtCore.QRect(50, 120, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mul_left_textEdit.setFont(font)
        self.mul_left_textEdit.setAcceptRichText(False)
        self.mul_left_textEdit.setObjectName("mul_left_textEdit")
        self.mul_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mul_right_textEdit.setGeometry(QtCore.QRect(300, 120, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mul_right_textEdit.setFont(font)
        self.mul_right_textEdit.setAcceptRichText(False)
        self.mul_right_textEdit.setObjectName("mul_right_textEdit")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(500, 120, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(250, 170, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.div_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.div_eq_textEdit.setGeometry(QtCore.QRect(530, 170, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.div_eq_textEdit.setFont(font)
        self.div_eq_textEdit.setReadOnly(True)
        self.div_eq_textEdit.setAcceptRichText(False)
        self.div_eq_textEdit.setObjectName("div_eq_textEdit")
        self.div_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.div_left_textEdit.setGeometry(QtCore.QRect(50, 170, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.div_left_textEdit.setFont(font)
        self.div_left_textEdit.setAcceptRichText(False)
        self.div_left_textEdit.setObjectName("div_left_textEdit")
        self.div_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.div_right_textEdit.setGeometry(QtCore.QRect(300, 170, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.div_right_textEdit.setFont(font)
        self.div_right_textEdit.setAcceptRichText(False)
        self.div_right_textEdit.setObjectName("div_right_textEdit")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(500, 170, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(250, 220, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.xor_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.xor_eq_textEdit.setGeometry(QtCore.QRect(530, 220, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xor_eq_textEdit.setFont(font)
        self.xor_eq_textEdit.setReadOnly(True)
        self.xor_eq_textEdit.setAcceptRichText(False)
        self.xor_eq_textEdit.setObjectName("xor_eq_textEdit")
        self.xor_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.xor_left_textEdit.setGeometry(QtCore.QRect(50, 220, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xor_left_textEdit.setFont(font)
        self.xor_left_textEdit.setAcceptRichText(False)
        self.xor_left_textEdit.setObjectName("xor_left_textEdit")
        self.xor_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.xor_right_textEdit.setGeometry(QtCore.QRect(300, 220, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xor_right_textEdit.setFont(font)
        self.xor_right_textEdit.setAcceptRichText(False)
        self.xor_right_textEdit.setObjectName("xor_right_textEdit")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(500, 220, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(250, 260, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.and_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.and_eq_textEdit.setGeometry(QtCore.QRect(530, 260, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.and_eq_textEdit.setFont(font)
        self.and_eq_textEdit.setReadOnly(True)
        self.and_eq_textEdit.setAcceptRichText(False)
        self.and_eq_textEdit.setObjectName("and_eq_textEdit")
        self.and_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.and_left_textEdit.setGeometry(QtCore.QRect(50, 260, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.and_left_textEdit.setFont(font)
        self.and_left_textEdit.setAcceptRichText(False)
        self.and_left_textEdit.setObjectName("and_left_textEdit")
        self.and_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.and_right_textEdit.setGeometry(QtCore.QRect(300, 260, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.and_right_textEdit.setFont(font)
        self.and_right_textEdit.setAcceptRichText(False)
        self.and_right_textEdit.setObjectName("and_right_textEdit")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(500, 260, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(250, 300, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.orr_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.orr_eq_textEdit.setGeometry(QtCore.QRect(530, 300, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.orr_eq_textEdit.setFont(font)
        self.orr_eq_textEdit.setReadOnly(True)
        self.orr_eq_textEdit.setAcceptRichText(False)
        self.orr_eq_textEdit.setObjectName("orr_eq_textEdit")
        self.orr_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.orr_left_textEdit.setGeometry(QtCore.QRect(50, 300, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.orr_left_textEdit.setFont(font)
        self.orr_left_textEdit.setAcceptRichText(False)
        self.orr_left_textEdit.setObjectName("orr_left_textEdit")
        self.orr_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.orr_right_textEdit.setGeometry(QtCore.QRect(300, 300, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.orr_right_textEdit.setFont(font)
        self.orr_right_textEdit.setAcceptRichText(False)
        self.orr_right_textEdit.setObjectName("orr_right_textEdit")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(500, 300, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(250, 340, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.shl_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shl_eq_textEdit.setGeometry(QtCore.QRect(530, 340, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shl_eq_textEdit.setFont(font)
        self.shl_eq_textEdit.setReadOnly(True)
        self.shl_eq_textEdit.setAcceptRichText(False)
        self.shl_eq_textEdit.setObjectName("shl_eq_textEdit")
        self.shl_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shl_left_textEdit.setGeometry(QtCore.QRect(50, 340, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shl_left_textEdit.setFont(font)
        self.shl_left_textEdit.setAcceptRichText(False)
        self.shl_left_textEdit.setObjectName("shl_left_textEdit")
        self.shl_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shl_right_textEdit.setGeometry(QtCore.QRect(300, 340, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shl_right_textEdit.setFont(font)
        self.shl_right_textEdit.setAcceptRichText(False)
        self.shl_right_textEdit.setObjectName("shl_right_textEdit")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(500, 340, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setGeometry(QtCore.QRect(250, 380, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.shr_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shr_eq_textEdit.setGeometry(QtCore.QRect(530, 380, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shr_eq_textEdit.setFont(font)
        self.shr_eq_textEdit.setReadOnly(True)
        self.shr_eq_textEdit.setAcceptRichText(False)
        self.shr_eq_textEdit.setObjectName("shr_eq_textEdit")
        self.shr_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shr_left_textEdit.setGeometry(QtCore.QRect(50, 380, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shr_left_textEdit.setFont(font)
        self.shr_left_textEdit.setAcceptRichText(False)
        self.shr_left_textEdit.setObjectName("shr_left_textEdit")
        self.shr_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.shr_right_textEdit.setGeometry(QtCore.QRect(300, 380, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.shr_right_textEdit.setFont(font)
        self.shr_right_textEdit.setAcceptRichText(False)
        self.shr_right_textEdit.setObjectName("shr_right_textEdit")
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(500, 380, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.tab)
        self.label_19.setGeometry(QtCore.QRect(10, 470, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.mod_eq_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mod_eq_textEdit.setGeometry(QtCore.QRect(530, 420, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mod_eq_textEdit.setFont(font)
        self.mod_eq_textEdit.setReadOnly(True)
        self.mod_eq_textEdit.setAcceptRichText(False)
        self.mod_eq_textEdit.setObjectName("mod_eq_textEdit")
        self.mod_left_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mod_left_textEdit.setGeometry(QtCore.QRect(50, 420, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mod_left_textEdit.setFont(font)
        self.mod_left_textEdit.setAcceptRichText(False)
        self.mod_left_textEdit.setObjectName("mod_left_textEdit")
        self.mod_right_textEdit = QtWidgets.QTextEdit(self.tab)
        self.mod_right_textEdit.setGeometry(QtCore.QRect(300, 420, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mod_right_textEdit.setFont(font)
        self.mod_right_textEdit.setAcceptRichText(False)
        self.mod_right_textEdit.setObjectName("mod_right_textEdit")
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(500, 420, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.ord_ord_textEdit = QtWidgets.QTextEdit(self.tab)
        self.ord_ord_textEdit.setGeometry(QtCore.QRect(50, 470, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ord_ord_textEdit.setFont(font)
        self.ord_ord_textEdit.setAcceptRichText(False)
        self.ord_ord_textEdit.setObjectName("ord_ord_textEdit")
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setGeometry(QtCore.QRect(250, 470, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.uord_ord_textEdit = QtWidgets.QTextEdit(self.tab)
        self.uord_ord_textEdit.setGeometry(QtCore.QRect(300, 470, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.uord_ord_textEdit.setFont(font)
        self.uord_ord_textEdit.setAcceptRichText(False)
        self.uord_ord_textEdit.setObjectName("uord_ord_textEdit")
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(250, 420, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(490, 470, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.uleb_leb_textEdit = QtWidgets.QTextEdit(self.tab)
        self.uleb_leb_textEdit.setGeometry(QtCore.QRect(300, 520, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.uleb_leb_textEdit.setFont(font)
        self.uleb_leb_textEdit.setAcceptRichText(False)
        self.uleb_leb_textEdit.setObjectName("uleb_leb_textEdit")
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(10, 520, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.label_26 = QtWidgets.QLabel(self.tab)
        self.label_26.setGeometry(QtCore.QRect(250, 520, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.leb_leb_textEdit = QtWidgets.QTextEdit(self.tab)
        self.leb_leb_textEdit.setGeometry(QtCore.QRect(50, 520, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.leb_leb_textEdit.setFont(font)
        self.leb_leb_textEdit.setAcceptRichText(False)
        self.leb_leb_textEdit.setObjectName("leb_leb_textEdit")
        self.left_not_textEdit = QtWidgets.QTextEdit(self.tab)
        self.left_not_textEdit.setGeometry(QtCore.QRect(120, 610, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.left_not_textEdit.setFont(font)
        self.left_not_textEdit.setAcceptRichText(False)
        self.left_not_textEdit.setObjectName("left_not_textEdit")
        self.label_27 = QtWidgets.QLabel(self.tab)
        self.label_27.setGeometry(QtCore.QRect(20, 610, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.tab)
        self.label_28.setGeometry(QtCore.QRect(340, 610, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.right_not_textEdit = QtWidgets.QTextEdit(self.tab)
        self.right_not_textEdit.setGeometry(QtCore.QRect(490, 610, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.right_not_textEdit.setFont(font)
        self.right_not_textEdit.setAcceptRichText(False)
        self.right_not_textEdit.setObjectName("right_not_textEdit")
        self.hex_ord_textEdit = QtWidgets.QTextEdit(self.tab)
        self.hex_ord_textEdit.setGeometry(QtCore.QRect(530, 470, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hex_ord_textEdit.setFont(font)
        self.hex_ord_textEdit.setAcceptRichText(False)
        self.hex_ord_textEdit.setObjectName("hex_ord_textEdit")
        self.hex_leb_textEdit = QtWidgets.QTextEdit(self.tab)
        self.hex_leb_textEdit.setGeometry(QtCore.QRect(530, 520, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hex_leb_textEdit.setFont(font)
        self.hex_leb_textEdit.setAcceptRichText(False)
        self.hex_leb_textEdit.setObjectName("hex_leb_textEdit")
        self.line_note = QtWidgets.QLabel(self.tab)
        self.line_note.setGeometry(QtCore.QRect(40, 650, 631, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.line_note.setFont(font)
        self.line_note.setText("")
        self.line_note.setObjectName("line_note")
        self.label_30 = QtWidgets.QLabel(self.tab)
        self.label_30.setGeometry(QtCore.QRect(490, 560, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.tab)
        self.label_31.setGeometry(QtCore.QRect(10, 560, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.hex_float_textEdit = QtWidgets.QTextEdit(self.tab)
        self.hex_float_textEdit.setGeometry(QtCore.QRect(530, 560, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hex_float_textEdit.setFont(font)
        self.hex_float_textEdit.setAcceptRichText(False)
        self.hex_float_textEdit.setObjectName("hex_float_textEdit")
        self.float_float_textEdit = QtWidgets.QTextEdit(self.tab)
        self.float_float_textEdit.setGeometry(QtCore.QRect(50, 560, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.float_float_textEdit.setFont(font)
        self.float_float_textEdit.setAcceptRichText(False)
        self.float_float_textEdit.setObjectName("float_float_textEdit")
        self.double_float_textEdit = QtWidgets.QTextEdit(self.tab)
        self.double_float_textEdit.setGeometry(QtCore.QRect(300, 560, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.double_float_textEdit.setFont(font)
        self.double_float_textEdit.setAcceptRichText(False)
        self.double_float_textEdit.setObjectName("double_float_textEdit")
        self.label_32 = QtWidgets.QLabel(self.tab)
        self.label_32.setGeometry(QtCore.QRect(240, 560, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.tab)
        self.label_33.setGeometry(QtCore.QRect(490, 520, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        TabWidget.addTab(self.tab, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "空道 十六进制 计算器 v3.0 "))
        self.label.setText(_translate("TabWidget", "+"))
        self.label_2.setText(_translate("TabWidget", "="))
        self.label_3.setText(_translate("TabWidget", "-"))
        self.label_4.setText(_translate("TabWidget", "="))
        self.label_5.setText(_translate("TabWidget", "*"))
        self.label_6.setText(_translate("TabWidget", "="))
        self.label_7.setText(_translate("TabWidget", "/"))
        self.label_8.setText(_translate("TabWidget", "="))
        self.label_9.setText(_translate("TabWidget", "^"))
        self.label_10.setText(_translate("TabWidget", "="))
        self.label_11.setText(_translate("TabWidget", "&"))
        self.label_12.setText(_translate("TabWidget", "="))
        self.label_13.setText(_translate("TabWidget", "|"))
        self.label_14.setText(_translate("TabWidget", "="))
        self.label_15.setText(_translate("TabWidget", "<<"))
        self.label_16.setText(_translate("TabWidget", "="))
        self.label_17.setText(_translate("TabWidget", ">>"))
        self.label_18.setText(_translate("TabWidget", "="))
        self.label_19.setText(_translate("TabWidget", "ord"))
        self.label_20.setText(_translate("TabWidget", "="))
        self.label_21.setText(_translate("TabWidget", "uord"))
        self.label_22.setText(_translate("TabWidget", "%"))
        self.label_23.setText(_translate("TabWidget", "hex"))
        self.label_24.setText(_translate("TabWidget", "leb"))
        self.label_26.setText(_translate("TabWidget", "uleb"))
        self.label_27.setText(_translate("TabWidget", "value(hex)"))
        self.label_28.setText(_translate("TabWidget", "not value(hex)"))
        self.label_30.setText(_translate("TabWidget", "hex"))
        self.label_31.setText(_translate("TabWidget", "float"))
        self.label_32.setText(_translate("TabWidget", "double"))
        self.label_33.setText(_translate("TabWidget", "hex"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1"))