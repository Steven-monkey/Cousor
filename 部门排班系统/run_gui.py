#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部门排班系统 - 图形界面启动入口

双击运行或执行：python run_gui.py
会启动图形界面，在窗口里填组员、选时间，点"生成排班表"即可。
"""
import sys
import os

# 把 src 目录加入 Python 的搜索路径，这样 import paiban 才能找到
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from paiban.gui import main

if __name__ == "__main__":
    main()
