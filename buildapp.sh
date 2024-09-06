#!/bin/sh
MYDIR=`dirname $0`
cd $MYDIR
rm -R dist/*
pyinstaller --onefile --noconsole --noupx --strip -w -y main.py --hidden-import http.cookies --icon=ui/Calculator.icns
###为了兼容低版本系统的osx pyinstaller 命令,所以不能使用 -n 参数只能使用mv命令

mv dist/main dist/calc
mv dist/main.app dist/calc.app
