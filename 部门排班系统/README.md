# 部门排班系统

自动生成周末和法定节假日的值班排班表，适合 Python 初学者学习工程目录和代码结构。

## 快速开始

1. **安装依赖**
   ```
   pip install -r requirements.txt
   ```

2. **运行**
   - 图形界面：双击 `启动排班界面.bat` 或执行 `python run_gui.py`
   - 命令行：执行 `python run_cli.py`

3. **生成结果**：`排班表_2024年1-12月.xlsx`

## 项目结构（初学必看）

```
部门排班系统/
├── README.md           # 项目说明（你正在看的）
├── requirements.txt    # 依赖列表
├── run_gui.py          # 图形界面入口
├── run_cli.py          # 命令行入口
├── 启动排班界面.bat     # 双击启动
├── 安装依赖.bat         # 双击安装依赖
└── src/
    └── paiban/         # 核心代码包
        ├── __init__.py # 包标识，导出函数
        ├── core.py     # 排班逻辑（日期、分配、导出）
        ├── cli.py      # 命令行交互
        └── gui.py      # 图形界面
```

## 主要功能

- 识别周末、法定节假日，自动排除调休日
- 劳动节/国庆节分段安排，连休固定同一组
- 每组每月不超过 4 天，避免连续值班
- 可接续上一年的排班顺序

## 技术栈

- Python 3.6+
- pandas、xlsxwriter（Excel）
- chinese_calendar（节假日）

代码里已有详细注释，适合边看边学。
