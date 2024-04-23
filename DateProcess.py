# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2024/4/13 11:07   
# @Author  : 李清水            
# @File    : DateProcess.py       
# @Description : 定义了DateProcessClass的属性和方法，定义了DateProcessInterface接口

# 使用typing模块提供的复合注解功能
from typing import List
# 具体实现需要的依赖库
import math
import matplotlib.pyplot as plt
import random
# 引入枚举类
from enum import Enum


# 全局变量，记录三个周期的采样值
FileterLength   = 3
DataList        = [0] * FileterLength
def AverageFilter(value):
    '''
    平均值滤波函数，实现三个周期的传感器采样值计算平均值
    :param value: 当前采样值
    :return: 滤波后的传感器数值
    '''
    global DataList
    # 临时变量，存储列表中数据之和
    sum = 0
    for i in range(FileterLength-1):
        # 实现列表的移位操作
        DataList[i] = DataList[i+1]
        # 实现列表求和
        sum += DataList[i]
    DataList[FileterLength-1] = value
    sum += DataList[FileterLength-1]
    average = sum / len(DataList)
    return average

AverageFilter.description = ("The average value filter function realizes the calculation of the average value "
                             "of the sensor sample value for three periods")


# # 使用标准类定义数据处理接口
# class DateProcessInterface(object):
#     def __init__(self,DateList:List[int],FilterLength:int):
#         '''
#         初始化方法
#         :param DateList: 数据列表
#         :param FilterLength: 对多少个点做数据滤波
#         '''
#         raise NotImplementedError
#     def DateFilter(self)->List:
#         '''
#         数据滤波
#         :return: List
#         '''
#         raise NotImplementedError
#     def DateCalMax(self)->int:
#         '''
#         计算数据最大值
#         :return: int
#         '''
#         pass
#     def DateCalMin(self)->int:
#         '''
#         计算最小值
#         :return: int
#         '''
#         pass

# from abc import ABCMeta, abstractmethod
#
# # 使用抽象基类定义数据处理接口
# class DateProcessInterface(metaclass=ABCMeta):
#     def __init__(self,DateList:List[int],FilterLength:int):
#         '''
#         初始化方法
#         :param DateList: 数据列表
#         :param FilterLength: 对多少个点做数据滤波
#         '''
#         pass
#
#     @abstractmethod
#     def DateFilter(self)->List:
#         '''
#         抽象方法，数据滤波
#         :return: List
#         '''
#         pass
#
#     @abstractmethod
#     def DateCalMax(self)->int:
#         '''
#         抽象方法，计算数据最大值
#         :return: int
#         '''
#         pass
#
#     @abstractmethod
#     def DateCalMin(self)->int:
#         '''
#         抽象方法，计算最小值
#         :return: int
#         '''
#         pass


# 滤波器类型枚举类
class FilterType(Enum):
    AVERAGEFILTER = 0
    LPFFILTER = 1


# # 创建一个具体类来继承于DateProcessInterface
# class DateProcessClass(DateProcessInterface):
#     def __init__(self,DateList:List[int],FilterLength:int):
#         self.DateList       = DateList
#         self.FilterLength   = FilterLength
#         self.TempList       = [0] * (self.FilterLength)
#     def DateFilter(self)->List:
#         # 遍历DateList
#         for index,value in enumerate(self.DateList):
#             # 把每个值都当成传入的新的传感器的值
#             NowValue = value
#             # 表示列表求和的变量
#             sum = 0
#             for i in range(self.FilterLength-1):
#                 # 实现列表的移位操作
#                 self.TempList[i] = self.TempList[i + 1]
#                 # 实现列表求和
#                 sum += self.TempList[i]
#             self.TempList[self.FilterLength-1] = NowValue
#             sum += self.TempList[self.FilterLength - 1]
#             # 求平均值
#             average = sum / self.FilterLength
#             # 将计算得到的平均值替换原始值
#             self.DateList[index] = average
#         # 计算完成后将TempList中元素清零
#         self.TempList = [0] * (self.FilterLength)
#         return self.DateList
#     def DateCalMax(self)->int:
#         max_value = max(self.DateList)
#         return int(max_value)
#     def DateCalMin(self)->int:
#         min_value = min(self.DateList)
#         return int(min_value)

# 导入接口相关的第三方拓展库
from zope.interface import Interface
from zope.interface.declarations import implementer

# 定义接口
class DateProcessInterface(Interface):
    def __init__(self, DateList: List[int], FilterLength: int):
        '''
        初始化方法
        :param DateList: 数据列表
        :param FilterLength: 对多少个点做数据滤波
        '''
        pass

    def DateFilter(self) -> List:
        '''
        抽象方法，数据滤波
        :return: List
        '''
        pass

    def DateCalMax(self) -> int:
        '''
        抽象方法，计算数据最大值
        :return: int
        '''
        pass

    def DateCalMin(self) -> int:
        '''
        抽象方法，计算最小值
        :return: int
        '''
        pass

# 使用具体类继承接口
@implementer(DateProcessInterface)
class DateProcessClass():
    def __init__(self, DateList: List[int], FilterLength: int):
        self.DateList = DateList
        self.FilterLength = FilterLength
        self.TempList = [0] * (self.FilterLength)

    def DateFilter(self) -> List:
        # 遍历DateList
        for index, value in enumerate(self.DateList):
            # 把每个值都当成传入的新的传感器的值
            NowValue = value
            # 表示列表求和的变量
            sum = 0
            for i in range(self.FilterLength - 1):
                # 实现列表的移位操作
                self.TempList[i] = self.TempList[i + 1]
                # 实现列表求和
                sum += self.TempList[i]
            self.TempList[self.FilterLength - 1] = NowValue
            sum += self.TempList[self.FilterLength - 1]
            # 求平均值
            average = sum / self.FilterLength
            # 将计算得到的平均值替换原始值
            self.DateList[index] = average
        # 计算完成后将TempList中元素清零
        self.TempList = [0] * (self.FilterLength)
        return self.DateList

    def DateCalMax(self) -> int:
        max_value = max(self.DateList)
        return int(max_value)

    def DateCalMin(self) -> int:
        min_value = min(self.DateList)
        return int(min_value)

print(type(DateProcessInterface))
print(type(DateProcessClass), DateProcessClass.__bases__)


if __name__ == '__main__':
    # 创建l的索引列表，主要提供给plot函数作为x轴坐标
    index = [x for x in range(0, 100)]
    # 生成一个正弦序列
    originalsignal = [math.sin(x) * 10 for x in range(0, 100)]
    # 生成随机数序列，模拟噪声
    noise = [random.uniform(0, 5) for x in range(0, 100)]
    # 将两个列表中的元素相加
    signal = [x + y for x, y in zip(originalsignal, noise)]
    # 创建DateProcessClass类，传入signal.copy()
    # 通过创建signal的拷贝序列，从而不改变l的原始数据
    s = DateProcessClass(signal.copy(), 10)
    print(type(s))
    # 进行数据滤波
    filtersignal = s.DateFilter()
    # 曲线绘图
    plt.plot(index, signal, 'b')
    plt.plot(index, filtersignal, 'r')
    # 显示图像
    plt.show()
    # 打印信号最大值
    print("Signal Max value:", s.DateCalMax())
    # 打印信号最小值
    print("Signal Min value:", s.DateCalMin())
    # 打印接口和具体类的关系
    print(issubclass(DateProcessClass, DateProcessInterface))
    print(isinstance(DateProcessClass, DateProcessInterface))






