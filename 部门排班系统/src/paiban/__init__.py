"""
部门排班系统 - paiban 包

Python 的包（package）就是一个带 __init__.py 的文件夹。
这里把 core 里的核心函数"导出"出去，别的文件可以写：
  from paiban import get_all_schedule_dates, create_schedule, export_to_excel
"""
from .core import (
    get_all_schedule_dates,
    create_schedule,
    export_to_excel,
)

__all__ = [
    "get_all_schedule_dates",
    "create_schedule",
    "export_to_excel",
]
