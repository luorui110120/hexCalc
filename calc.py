# -*- coding: utf-8 -*-
# python 3.9
# Author: By 空道
# Created on 10:19 2020/12/5

from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
import re
import os
from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps

def allSelectText(text_obj):
    text_obj.selection_range(0, len(text_obj.get())) 
def calc_func(leftValue,rightValue,operator, outVlaue):
    leftint= 0
    rightint=0
    leftstr=leftValue.get()
    rightstr=rightValue.get()
    data = leftstr.strip() + rightstr.strip()
    if re.match('\A[0-9a-fxA-FX]+\Z',data) is None:
        outVlaue.set("illegal character")
    if(leftValue and len(leftstr.strip()) > 0):
        leftint = int(leftstr.strip() , 16)
    if(rightValue and len(rightstr.strip()) > 0):
        rightint = int(rightstr.strip() , 16)
    
    armcode='int(%d%s%d)'%(leftint,operator,rightint)
    outend = eval(armcode)
    outVlaue.set("%X"%(outend & ((1 << 64) - 1)))
def frameUI(master, operator):
    fm1 = Frame(master)
    addLeftValue = StringVar()
    addLeft = Entry(fm1, textvariable=addLeftValue)
    addLeft.pack(side=LEFT, fill=BOTH, expand=True)
    Label(fm1, text=operator,width=5).pack(side=LEFT, fill=BOTH, expand=True)
    addRightValue = StringVar()
    addRight = Entry(fm1, textvariable=addRightValue)
    addRight.pack(side=LEFT, fill=BOTH, expand=True)
    Label(fm1, text='=').pack(side=LEFT, fill=BOTH, expand=True)
    addOutValue = StringVar()
    addOut = Entry(fm1, textvariable=addOutValue,state='readonly')
    addOut.pack(side=LEFT)
    addLeft.bind('<KeyRelease>', lambda event:calc_func(leftValue=addLeftValue,rightValue=addRightValue,operator=operator,outVlaue=addOutValue))
    addRight.bind('<KeyRelease>', lambda event:calc_func(leftValue=addLeftValue,rightValue=addRightValue,operator=operator,outVlaue=addOutValue))
    addLeft.bind("<Command-a>", lambda event:allSelectText(text_obj=addLeft))
    addRight.bind("<Command-a>", lambda event:allSelectText(text_obj=addRight))
    addOut.bind("<Command-a>", lambda event:allSelectText(text_obj=addOut))
    return fm1

def func_ord_to_hex(leftValue,rightValue):
    leftstr=leftValue.get()
    if re.match('\A[0-9a-fxA-FX]+\Z',leftstr) is None:
        rightValue.set("illegal character")
    if(leftValue and len(leftstr.strip()) > 0):
        leftint = int(leftstr.strip() , 10)
    rightValue.set('%X'%leftint)
def func_hex_to_ord(leftValue,rightValue):
    rightstr=rightValue.get()
    if re.match('\A[0-9a-fxA-FX]+\Z',rightstr) is None:
        leftValue.set("illegal character")
    if(rightValue and len(rightstr.strip()) > 0):
        rightint = int(rightstr.strip() , 16)
    leftValue.set('%d'%rightint)

def func_not_left_value(leftValue,rightValue):
    leftstr=leftValue.get()
    if re.match('\A[0-9a-fxA-FX]+\Z',leftstr) is None:
        rightValue.set("illegal character")
    if(leftValue and len(leftstr.strip()) > 0):
        leftint = int(leftstr.strip() , 16)
    rightValue.set("%X"%(~leftint & ((1 << 64) - 1)))
def func_not_right_value(leftValue,rightValue):
    rightstr=rightValue.get()
    if re.match('\A[0-9a-fxA-FX]+\Z',rightstr) is None:
        leftValue.set("illegal character")
    if(rightValue and len(rightstr.strip()) > 0):
        rightint = int(rightstr.strip() , 16)
    leftValue.set("%X"%(~rightint & ((1 << 64) - 1)))
def frameHexUI(master):
    fm1 = Frame(master)
    Label(fm1, text='ord').pack(side=LEFT, fill=BOTH, expand=True)
    addLeftValue = StringVar()
    addLeft = Entry(fm1, textvariable=addLeftValue)
    addLeft.pack(side=LEFT, fill=BOTH, expand=True)
    Label(fm1, text='hex').pack(side=LEFT, fill=BOTH, expand=True)
    addRightValue = StringVar()
    addRight = Entry(fm1, textvariable=addRightValue)
    addRight.pack(side=LEFT, fill=BOTH, expand=True)
    
    addLeft.bind('<KeyRelease>', lambda event:func_ord_to_hex(leftValue=addLeftValue,rightValue=addRightValue))
    addRight.bind('<KeyRelease>', lambda event:func_hex_to_ord(leftValue=addLeftValue,rightValue=addRightValue))
    addLeft.bind("<Command-a>", lambda event:allSelectText(text_obj=addLeft))
    addRight.bind("<Command-a>", lambda event:allSelectText(text_obj=addRight))
    return fm1
def frameNotUI(master):
    fm1 = Frame(master)
    Label(fm1, text='value(hex)').pack(side=LEFT, fill=BOTH, expand=True)
    addLeftValue = StringVar()
    addLeft = Entry(fm1, textvariable=addLeftValue)
    addLeft.pack(side=LEFT, fill=BOTH, expand=True)
    Label(fm1, text='not value(hex)').pack(side=LEFT, fill=BOTH, expand=True)
    addRightValue = StringVar()
    addRight = Entry(fm1, textvariable=addRightValue)
    addRight.pack(side=LEFT, fill=BOTH, expand=True)
    
    addLeft.bind('<KeyRelease>', lambda event:func_not_left_value(leftValue=addLeftValue,rightValue=addRightValue))
    addRight.bind('<KeyRelease>', lambda event:func_not_right_value(leftValue=addLeftValue,rightValue=addRightValue))
    addLeft.bind("<Command-a>", lambda event:allSelectText(text_obj=addLeft))
    addRight.bind("<Command-a>", lambda event:allSelectText(text_obj=addRight))
    return fm1

def center_window(root, w, h):
    # 获取屏幕 宽、高
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
def UI_init(root):
    addFrame = frameUI(root,'+')
    subFrame = frameUI(root,'-')
    mulFrame = frameUI(root,'*')
    divFrame = frameUI(root,'/')
    xorFrame = frameUI(root,'^')
    andFrame = frameUI(root,'&')
    orFrame = frameUI(root,'|')
    shlFrame = frameUI(root,'<<')
    shrFrame = frameUI(root,'>>')
    ordToHexFrame = frameHexUI(root)
    notToValueFrame = frameNotUI(root)
    addFrame.pack(side=TOP,fill=X, expand=YES)
    subFrame.pack(side=TOP,fill=X, expand=YES)
    mulFrame.pack(side=TOP,fill=X, expand=YES)
    divFrame.pack(side=TOP,fill=X, expand=YES)
    xorFrame.pack(side=TOP,fill=X, expand=YES)
    andFrame.pack(side=TOP,fill=X, expand=YES)
    orFrame.pack(side=TOP,fill=X, expand=YES)
    shlFrame.pack(side=TOP,fill=X, expand=YES)
    shrFrame.pack(side=TOP,fill=X, expand=YES)
    ordToHexFrame.pack(side=TOP,fill=X, expand=YES)
    notToValueFrame.pack(side=TOP,fill=X, expand=YES)
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None, title='title'):
        Frame.__init__(self, master)
        self.master.title(title)
        self.master.geometry('700x400')
        self.createWidgets()
 
    def createWidgets(self):
        self.top = self.winfo_toplevel()
 
        self.style = Style()
 
        self.TabStrip_book = Notebook(self.top)
        self.TabStrip_book.place(relx=0, rely=0, relwidth=1, relheight=1)
 
        # self.TabStrip1__Tab1 = Frame(self.TabStrip_book)
        # self.TabStrip1__Tab1Lbl =UI_init(self.TabStrip1__Tab1)
        # self.TabStrip_book.add(self.TabStrip1__Tab1, text='我的快玩')
 
        # self.TabStrip1__Tab2 = Frame(self.TabStrip_book)
        # self.TabStrip1__Tab2Lbl = UI_init(self.TabStrip1__Tab2)
        # self.TabStrip_book.add(self.TabStrip1__Tab2, text='找游戏')
        for i in range(5):
            self.TabStrip__Tab = Frame(self.TabStrip_book)
            self.TabStrip__UI = UI_init(self.TabStrip__Tab)
            self.TabStrip_book.add(self.TabStrip__Tab, text='table-%d'%i)
def main():
    window = Tk()
    ### 为了实现多标签页
    Application_ui(window, "空道 十六进制 计算器 v2.0")
    #### //将窗口显示在最前面
    window.lift()
    window.attributes('-topmost',True)
    window.after_idle(window.attributes,'-topmost',False)
    ##### //将主窗口居中
    window.update()
    center_window(window,window.winfo_width(), window.winfo_height())
    ###//程序启动获取焦点
    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
    app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    ## //下面这种命令行的方式容易出错
    #os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    window.mainloop()

main()