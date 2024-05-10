# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2024/5/9 14:04   
# @Author  : 李清水            
# @File    : Parallel.py       
# @Description : Python并行相关程序

# 串口相关
import serial
# 并行并发相关
from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue , SimpleQueue
from multiprocessing import Lock
# 数学计算相关
import math
import random
# 时间操作相关
import time
# 曲线作图相关库
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
# 使用typing模块提供的复合注解功能
from typing import List


# 主机多进程类
class MasterProcess(Process):
    '''
        主机多进程类
    '''
    # 类变量：
    #   START_CMD       - 开启命令      -0
    #   STOP_CMD        - 关闭命令      -1
    #   SENDID_CMD      - 发送ID命令    -2
    #   SENDVALUE_CMD   - 发送数据命令   -3
    START_CMD, STOP_CMD, SENDID_CMD, SENDVALUE_CMD = (0, 1, 2, 3)

    def __init__(self,
                 lock,
                 Queue,
                 simplequeue,
                 port:str = "COM17",
                 baudrate:int = 115200,
                 bytesize:int = serial.EIGHTBITS,
                 parity  :str = serial.PARITY_NONE,
                 stopbits:int = serial.STOPBITS_ONE):
        '''
        MasterProcess初始化函数
        :param lock: 互斥锁
        :param Queue: 队列
        :param port: 端口号
        :param baudrate: 波特率
        :param bytesize: 数据位
        :param parity: 校验位
        :param stopbits: 停止位
        '''
        self.lock               = lock
        self.Queue              = Queue
        self.simplequeue        = simplequeue
        self.dev                = serial.Serial()
        self.dev.port           = port
        self.dev.baudrate       = baudrate
        self.dev.bytesize       = bytesize
        self.dev.parity         = parity
        self.dev.stopbits       = stopbits
        # 设置读取timeout超时时间
        self.dev.timeout        = 0.3
        # 设置写入timeout超时时间
        self.dev.write_timeout  = 0.3
        # 数据缓存
        self.datalist           = []
        # 滤波器长度
        self.filterlength       = 3
        # 数据处理类实例
        self.dataprocessobj     = DateProcessClass(self.datalist,self.filterlength)
        # Process初始化方法
        Process.__init__(self)

    def StartMasterSerial(self):
        '''
        打开主机串口
        :return: None
        '''
        self.dev.open()

    def StopMasterSerial(self):
        '''
        停止主机串口
        :return: None
        '''
        self.dev.close()

    def __ReadMasterSerial(self):
        '''
        读取主机串口，私有方法
        :return data[int] : 读取的数据
        '''
        # 按行读取
        data = self.dev.readline()
        # 如果接收到字节的情况下，进行处理
        if data != b'':
            # 收到为二进制数据
            # 用utf-8编码将二进制数据解码为unicode字符串
            # 字符串转为int类型
            data = int(data.decode('utf-8', 'replace'))
        # 否则，设置data为-1
        else:
            data = -1
        return data

    def __WriteMasterSerial(self,write_data):
        '''
        写入主机串口，私有方法
        :param write_data: 写入的数据
        :return:
        '''
        # 非阻塞方式写入
        self.dev.write(write_data.encode())
        # 输出换行符
        # write的输入参数必须是bytes格式
        # 字符串数据需要encode()函数将其编码为二进制数据，然后才可以顺利发送
        # \r\n表示换行回车
        self.dev.write('\r\n'.encode())

    def RecvSensorID(self):
        '''
        读取传感器ID
        :return sensorid[int] : 读取的传感器id号
        '''
        sensorid = self.__ReadMasterSerial()
        return sensorid

    def RecvSensorValue(self):
        '''
        读取传感器数据值
        :return data[int] : 读取的传感器数据
        '''
        data = self.__ReadMasterSerial()
        return data

    def SendSensorCMD(self,cmd):
        '''
        主机发送命令
        :param cmd : MasterProcess中的类变量
        :return: None
        '''
        self.__WriteMasterSerial(str(cmd))

    def run(self):
        '''
        多进程start后运行的方法
        :return: None
        '''

        # 运行计数变量
        count = 0
        # 文件保存索引计数变量
        index = 0

        # 打开串口
        self.StartMasterSerial()

        self.lock.acquire()
        print(" Master Process Started ")
        self.lock.release()

        # 发送获取ID指令
        self.SendSensorCMD(self.SENDID_CMD)
        # 获取传感器ID号
        id = self.RecvSensorID()

        self.lock.acquire()
        print(" Recv Sensor ID : ", id)
        self.lock.release()

        while True:
            if count == 9:
                maxvalue = self.dataprocessobj.DateCalMax()
                minvalue = self.dataprocessobj.DateCalMin()
                self.lock.acquire()
                print("----------------------------------")
                print("Max Value: ", maxvalue)
                print("Min Value: ", minvalue)
                print("----------------------------------")
                self.lock.release()
                count = 0
            else:
                count = count + 1

            # 发送获取数据指令
            self.SendSensorCMD(self.SENDVALUE_CMD)

            self.lock.acquire()
            print("Master Send SENDVALUE_CMD")
            self.lock.release()

            # 接收传感器数据值
            data = self.RecvSensorValue()
            self.Queue.put(data)

            self.datalist.append(data)
            filterdata,filterdatalist = self.dataprocessobj.DateFilter()
            self.simplequeue.put(filterdata)

            self.lock.acquire()
            print("  Recv Sensor Data : ",data)
            self.lock.release()

            time.sleep(0.5)

class SensorThread(Thread):
    '''
    传感器多线程类
    '''

    # 类变量：
    #   RESPOND_MODE -响应模式-0
    #   LOOP_MODE    -循环模式-1
    # RESPOND_MODE,LOOP_MODE = (0,1)
    # 使用字典创建
    WORK_MODE = {"RESPOND_MODE": 0, "LOOP_MODE": 1}
    # 类变量：
    #   NONE_CMD        - 未接收数据    --1
    #   START_CMD       - 开启命令      -0
    #   STOP_CMD        - 关闭命令      -1
    #   SENDID_CMD      - 发送ID命令    -2
    #   SENDVALUE_CMD   - 发送数据命令   -3
    NONE_CMD, START_CMD, STOP_CMD, SENDID_CMD, SENDVALUE_CMD = (-1, 0, 1, 2, 3)

    def __init__(self, lock, port: str = "COM11", id: int = 0, state: int = WORK_MODE["RESPOND_MODE"]):
        '''
        传感器类的初始化
        :param lock: 互斥锁
        :param port: 端口号
        :param id: 传感器id
        :param state: 工作状态
        '''
        self.lock = lock

        self.sensorvalue    = 0
        self.sensorid       = id
        self.sensorstate    = state

        self.dev            = serial.Serial()
        self.dev.port       = port
        self.dev.baudrate   = 115200
        self.dev.bytesize   = serial.EIGHTBITS
        self.dev.parity     = serial.PARITY_NONE
        self.dev.stopbits   = serial.STOPBITS_ONE
        # 设置读取timeout超时时间
        self.dev.timeout = 0.3
        # 设置写入timeout超时时间
        self.dev.write_timeout = 0.3

        # Thread的初始化方法
        Thread.__init__(self)

    def StartSensorSerial(self):
        '''
        打开主机串口
        :return: None
        '''
        self.dev.open()

    def StopSensorSerial(self):
        '''
        停止主机串口
        :return: None
        '''
        self.dev.close()

    def __ReadSensorSerial(self):
        '''
        读取传感器串口，私有方法
        :return data[int] : 读取的数据
        '''
        # 按行读取
        data = self.dev.readline()
        # 如果接收到字节的情况下，进行处理
        if data != b'':
            # 收到为二进制数据
            # 用utf-8编码将二进制数据解码为unicode字符串
            # 字符串转为int类型
            data = int(data.decode('utf-8', 'replace'))
        # 否则，设置data为-1
        else:
            data = -1
        return data

    def __WriteSensorSerial(self,write_data):
        '''
        写入传感器串口，私有方法
        :param write_data: 写入的数据
        :return:
        '''
        # 非阻塞方式写入
        self.dev.write(write_data.encode())
        # 输出换行符
        # write的输入参数必须是bytes格式
        # 字符串数据需要encode()函数将其编码为二进制数据，然后才可以顺利发送
        # \r\n表示换行回车
        self.dev.write('\r\n'.encode())

    def SendSensorID(self):
        '''
        发送传感器ID号
        :return: None
        '''
        self.__WriteSensorSerial(str(self.sensorid))

    def SendSensorValue(self,data):
        '''
        发送传感器数据
        :param data: 待发送的数据
        :return: None
        '''
        self.__WriteSensorSerial(str(data))

    def RecvMasterCMD(self):
        '''
        接收主机命令
        :return cmd[int] : 待接收的命令
        '''
        cmd = self.__ReadSensorSerial()
        return cmd

    def run(self):
        '''
        多进程start后运行的方法
        :return: None
        '''

        # 初始化计数变量
        data_count = 0
        # 开启传感器
        self.StartSensorSerial()

        self.lock.acquire()
        print(" Sensor Thread Started ")
        self.lock.release()

        while True:
            # 生成数据
            data_count = data_count + 1
            # 原始信号
            signal = math.sin(data_count) * 10
            # 模拟噪声
            noise = random.uniform(0, 5)
            # 最终数据
            data = int(signal + noise)

            # 接收命令
            cmd = self.RecvMasterCMD()

            self.lock.acquire()
            print(" Sensor Recv CMD : ",cmd)
            self.lock.release()

            # 根据命令进行相关操作
            if cmd == SensorThread.STOP_CMD:
                # 如果接收到停止命令，停止传感器
                self.StopSensor()

                self.lock.acquire()
                # 输出提示信息
                print("Sensor stop work !!!")
                self.lock.release()

                return

            elif cmd == SensorThread.SENDID_CMD:
                # 如果接收到发送ID命令，发送传感器ID号
                self.SendSensorID()

            elif cmd == SensorThread.SENDVALUE_CMD:
                # 如果接收到发送数据命令，发送数据
                self.SendSensorValue(data)

                self.lock.acquire()
                # 输出提示信息
                print(" Sensor Send Data : ",data)
                self.lock.release()

            elif cmd == SensorThread.NONE_CMD:
                self.lock.acquire()
                # 如果没有接收到指令
                print("Not Recv cmd!!!")
                self.lock.release()

            # 延时0.5s
            time.sleep(0.5)

class PlotThread:
    def __init__(self,lock,queue,simplequeue,wintitle:str="Basic plotting examples",plottitle:str="Updating plot",width:int=1000,height:int=600):
        '''
        用于初始化PlotThread类
        :param wintitle:  窗口标题
        :param plottitle: 图层标题
        :param width:     窗口宽度
        :param height:    窗口高度
        '''
        self.lock               = lock
        self.queue              = queue
        self.simplequeue        = simplequeue
        # Qt应用实例对象
        self.app                = None
        # 窗口对象
        self.win                = None
        # 设置窗口标题
        self.title              = wintitle
        # 设置窗口尺寸
        self.width              = width
        self.height             = height
        # 传感器数据
        self.value              = 0
        # 存放滤波后数据
        self.filtervalue        = 0
        # 计数变量
        self.__count            = 0
        # 传感器数据缓存列表
        self.valuelist          = []
        # 传感器滤波数据缓存列表
        self.filtervaluelist    = []
        # 绘图曲线
        self.curve              = None
        # 滤波后绘图曲线
        self.filtercurve        = None
        # 图层对象
        self.plotob             = None
        # 图层标题
        self.plottitle          = plottitle
        # 定时器对象
        self.timer              = QtCore.QTimer()
        # 定时时间
        self.time               = 0
        # Qt应用和窗口初始化
        self.appinit()

        self.lock.acquire()
        print(" PlotClass Object Init Complete ")
        self.lock.release()

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
        # 原始数据-黄色曲线
        self.curve = self.plotob.plot(pen='y')
        # 滤波后数据-红色曲线
        self.filtercurve  = self.plotob.plot(pen='r')

    def GetValue(self,value,filtervalue):
        '''
        用于接收传感器数据，加入缓存列表
        :param value: 传感器数据
        :param filtervalue: 传感器滤波后数据
        :return: None
        '''
        self.value          = value
        self.valuelist.append(self.value)
        self.filtervalue    = filtervalue
        self.filtervaluelist.append(self.filtervalue)

    def DataUpdate(self):
        '''
        用于定时进行曲线更新,这里模拟绘制正弦曲线
        :return: None
        '''
        self.value = self.queue.get()
        self.filtervalue = self.simplequeue.get()
        self.GetValue(self.value,self.filtervalue)
        # 将数据转化为图形
        self.curve.setData(self.valuelist)
        self.filtercurve.setData(self.filtervaluelist)

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
        # 进入主事件循环并等待
        pg.exec()

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
        return average,self.DateList

    def DateCalMax(self) -> int:
        max_value = max(self.DateList)
        return int(max_value)

    def DateCalMin(self) -> int:
        min_value = min(self.DateList)
        return int(min_value)

if __name__ == "__main__":
    # 创建互斥锁
    lock    = Lock()
    # 创建消息队列
    queue   = Queue(5)
    # 创建消息队列
    simplequeue = SimpleQueue()

    # 创建进程实例
    m_process = MasterProcess(lock,queue,simplequeue,port = "COM17")
    # 创建线程实例
    s_thread  = SensorThread(lock,port="COM11", id=0, state=SensorThread.WORK_MODE["RESPOND_MODE"])
    # 创建绘图类实例
    p_thread  = PlotThread(lock,queue,simplequeue)

    # 启动进程
    m_process.start()
    # 开启线程，start方法以并发方式执行
    s_thread.start()
    # 启动p_thread的定时任务
    p_thread.SetUpdate(600)
