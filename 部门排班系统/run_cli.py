#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部门排班系统 - 命令行启动入口

执行：python run_cli.py
会在终端里一步步提示你输入组数、组员、时间等，然后生成排班表。
"""
import sys
import os

# 把 src 目录加入 Python 的搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from paiban.cli import main

if __name__ == "__main__":
    main()
