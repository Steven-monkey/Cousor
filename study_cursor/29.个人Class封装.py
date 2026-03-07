"""
个人 Class 封装 - 原版（带详细注释）
包含：Person 人物类、Calculator 计算器类
"""


# =============================================================================
# Person 人物类
# =============================================================================
class Persion:
    # 构造函数：创建对象时传入姓名、年龄、身高、体重
    def __init__(self, name, age, high, weight):
        # 属性：姓名
        self.name = name
        # 属性：年龄
        self.age = age
        # 属性：身高（cm）
        self.high = high
        # 属性：体重（kg）
        self.weight = weight

    # 方法：打印个人信息
    def show_info(self):
        print(
            f"我叫{self.name},今年{self.age}岁,身高{self.high}cm,体重{self.weight}kg")

    # 方法：创建一个关联的"女朋友"对象并返回
    def get_girlfriend(self, age, high, weight):
        # 返回新的 Person 对象，姓名为"xxx的女朋友"
        return Persion(self.name + "的女朋友", age, high, weight)


# 创建人物对象
persion = Persion("侯金双", 18, 180, 80)
# 调用 get_girlfriend，传入女朋友的年龄、身高、体重
girlfriend = persion.get_girlfriend(18, 170, 60)
# 打印女朋友信息
girlfriend.show_info()


# =============================================================================
# Calculator 计算器类
# =============================================================================
class Calculator:
    # 构造函数：初始化结果为 0
    def __init__(self):
        self.result = 0

    # 方法：加法
    def add(self, a, b):
        self.result = a + b
        return self.result

    # 方法：减法
    def sub(self, a, b):
        self.result = a - b
        return self.result

    # 方法：乘法
    def mul(self, a, b):
        self.result = a * b
        return self.result

    # 方法：除法（取整）
    def div(self, a, b):
        self.result = a / b
        return int(self.result)

    # 方法：打印当前结果
    def show_result(self):
        print(f"计算结果是:{self.result}")


# 创建计算器对象
clacu1 = Calculator()
# 调用各计算方法
print("加法结果：", clacu1.add(100, 20))
print("减法结果：", clacu1.sub(100, 20))
print("乘法结果：", clacu1.mul(100, 20))
print("除法结果：", clacu1.div(100, 20))
