# Python env   : Python 3.12 (parallel) (2)
# G:\miniconda\setup\envs\parallelpython.exe
# -*- coding: utf-8 -*-
# @Time    : 2024/2/16 11:09
# @Author  : 李清水
# @File    : Plot.py
# @Description : 定义了PlotClass的属性和方法

# 曲线作图相关库
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore
# 日志输出相关库
import logging

# 在配置下日志输出目标文件和日志格式
LOG_FORMAT="%(asctime)s-%(levelname)s-%(message)s"
logging.basicConfig(filename='my.log',level=logging.DEBUG,format=LOG_FORMAT)

class PlotClass:
    # 绘图类初始化
    def __init__(self,wintitle:str="Basic plotting examples",plottitle:str="Updating plot",width:int=1000,height:int=600):
        '''
        用于初始化Plot类
        :param wintitle:  窗口标题
        :param plottitle: 图层标题
        :param width:     窗口宽度
        :param height:    窗口高度
        '''
        # Qt应用实例对象
        self.app        = None
        # 窗口对象
        self.win        = None
        # 设置窗口标题
        self.title      = wintitle
        # 设置窗口尺寸
        self.width      = width
        self.height     = height
        # 传感器数据
        self.value      = 0
        # 计数变量
        self.__count    = 0
        # 传感器数据缓存列表
        self.valuelist  = []
        # 绘图曲线
        self.curve      = None
        # 图层对象
        self.plotob     = None
        # 图层标题
        self.plottitle  = plottitle
        # 定时器对象
        self.timer = QtCore.QTimer()
        # 定时时间
        self.time  = 0
        # Qt应用和窗口初始化
        self.appinit()

        print("PLOT INIT SUCCESS")
        logging.info("PLOT INIT SUCCESS")

    # 应用程序初始化
    def appinit(self):
        '''
        用于qt应用程序初始化，添加窗口、曲线和图层
        :return: None
        '''
        # 创建一个Qt应用，并返回该应用的实例对象
        self.app = pg.mkQApp("Plotting Example")
        # 生成多面板图形
        # show：(bool) 如果为 True，则在创建小部件后立即显示小部件。
        # title：(str 或 None)如果指定，则为此小部件设置窗口标题。
        self.win = pg.GraphicsLayoutWidget(show=True, title=self.title)
        # 设置窗口尺寸
        self.win.resize(self.width, self.height)
        # 进行窗口全局设置，setConfigOptions一次性配置多项参数
        # antialias启用抗锯齿，useNumba对图像进行加速
        pg.setConfigOptions(antialias=True, useNumba=True)

        # 添加图层
        self.plotob = self.win.addPlot(title=self.plottitle)
        # 添加曲线
        self.curve = self.plotob.plot(pen='y')

    # 接收数据
    def GetValue(self,value):
        '''
        用于接收传感器数据，加入缓存列表
        :param value: 传感器数据
        :return: None
        '''
        self.value = value
        self.valuelist.append(value)
        print("PLOT RECV DATA : "+str(self.value))
        logging.info("PLOT RECV DATA : "+str(self.value))

    # 更新曲线数据
    def DataUpdate(self):
        '''
        用于定时进行曲线更新,这里模拟绘制正弦曲线
        :return: None
        '''
        # 模拟绘制正弦曲线
        # 计数变量更新
        self.__count = self.__count + 0.1
        self.value = np.sin(self.__count)
        self.GetValue(self.value)
        # 将数据转化为图形
        self.curve.setData(self.valuelist)

    # 设置定时更新
    def SetUpdate(self,time:int = 100):
        '''
        设置定时更新任务
        :param time: 定时的时间
        :return: None
        '''
        # 定时器结束，触发DataUpdate方法
        self.timer.timeout.connect(self.DataUpdate)
        # 启动定时器
        self.timer.start(time)
        # 定时时间
        self.time = time
        print("PLOT SET UPDATA")
        logging.info("PLOT SET UPDATA")
        # 进入主事件循环并等待
        pg.exec()