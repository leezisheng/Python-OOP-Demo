# Python env   : Python 3.12 (parallel) (2)
# G:\miniconda\setup\envs\parallelpython.exe
# -*- coding: utf-8 -*-
# @Time    : 2024/2/16 11:10
# @Author  : 李清水
# @File    : FileIO.py
# @Description : 定义了传感器类和主机类的属性和方法
#                主程序，调用其他模块

# 队列相关
import queue
import random
# 日志输出相关库
import logging
# 引入枚举类
from enum import Enum
# 引用自定义模块
import FileIO
from FileIO import FileIOClass
from Plot   import PlotClass
from Serial import SerialClass
# 并行并发相关
from threading import Thread
from threading import Lock
from multiprocessing import Process
# 数学计算相关
import math
import random
# 时间操作相关
import time

# 日志设置
LOG_FORMAT="%(asctime)s-%(levelname)s-%(message)s"
logging.basicConfig(filename='my.log',level=logging.DEBUG,format=LOG_FORMAT)

# 定义一个ID号非法的异常
class InvalidIDError(Exception):
    pass

class SensorClass(SerialClass,Thread):
    '''
        传感器类，继承自SerialClass\Thread
    '''
    # 类变量：
    #   RESPOND_MODE -响应模式-0
    #   LOOP_MODE    -循环模式-1
    # RESPOND_MODE,LOOP_MODE = (0,1)
    # 使用字典创建
    WORK_MODE = {"RESPOND_MODE":0,"LOOP_MODE":1}
    # 类变量：
    #   NONE_CMD        - 未接收数据    --1
    #   START_CMD       - 开启命令      -0
    #   STOP_CMD        - 关闭命令      -1
    #   SENDID_CMD      - 发送ID命令    -2
    #   SENDVALUE_CMD   - 发送数据命令   -3
    NONE_CMD,START_CMD,STOP_CMD,SENDID_CMD,SENDVALUE_CMD = (-1,0,1,2,3)

    # 类的初始化
    def __init__(self,port:str = "COM11",id:int = 0,state:int = WORK_MODE["RESPOND_MODE"]):
        try:
            # 判断输入端口号是否为str类型
            if type(port) is not str:
                raise TypeError("InvalidPortError:",port)
            # 判断ID号是否在0~99之间
            if id < 0 or id > 99:
                # 触发异常后，后面的代码就不会再执行
                # 当传递给函数或方法的参数类型不正确或者参数的值不合法时，会引发此异常。
                raise InvalidIDError("InvalidIDError:",id)

            # 调用父类的初始化方法，super() 函数将父类和子类连接
            super().__init__(port)
            self.sensorvalue = 0
            self.sensorid    = id
            self.sensorstate = state
            print("Sensor Init")
            logging.info("Sensor Init")
            # Thread的初始化方法
            Thread.__init__(self)
        except TypeError:
            # 当发生异常时，输出如下语句，提醒用户重新输入端口号
            print("Input error com, Please try new com number")
        except InvalidIDError as e:
            # 当发生异常时，输出如下语句，提醒用户重新输入ID号
            print("Input error ID, Please try id : 0~99")
            print(e.args)

    @staticmethod
    # 判断传感器ID号是否正确：这里判断ID号是否在0到99之间
    def IsTrueID(id:int = 0):
        if id >= 0 and id <= 99:
            print("Sensor ID True")
            return True
        else:
            print("Sensor ID False")
            return False

    # 传感器上电初始化
    def InitSensor(self):
        # 传感器上电初始化工作
        # 同时输出ID号以及状态
        print("Sensor %d Init complete : %d"%(self.sensorid,self.sensorstate))
        logging.info("Sensor %d Init complete : %d"%(self.sensorid,self.sensorstate))

    # 开启传感器
    def StartSensor(self):
        super().OpenSerial()
        print("Sensor %d start serial %s "%(self.sensorid,self.dev.port))
        logging.info("Sensor %d start serial %s "%(self.sensorid,self.dev.port))

    # 停止传感器
    def StopSensor(self):
        super().CloseSerial()
        print("Sensor %d close serial %s " % (self.sensorid, self.dev.port))
        logging.info("Sensor %d close serial %s " % (self.sensorid, self.dev.port))

    # 发送传感器ID号
    def SendSensorID(self):
        super().WriteSerial(str(self.sensorid))
        print("Sensor %d send id "%self.sensorid)
        logging.info("Sensor %d send id "%self.sensorid)

    # 发送传感器数据
    def SendSensorValue(self,data):
        # 发送数据
        super().WriteSerial(str(data))
        print("Sensor %d send data  %d" % (self.sensorid,data))
        logging.info("Sensor %d send data  %d" % (self.sensorid,data))

    # 接收主机指令
    def RecvMasterCMD(self):
        cmd = super().ReadSerial()
        print("Sensor %d recv cmd %d " % (self.sensorid,cmd))
        logging.info("Sensor %d recv cmd %d " % (self.sensorid,cmd))
        return cmd

    # 多线程中用以表示线程活动的方法
    # run 方法中的所有代码（或者在这一方法内部调用的代码）都在一个单独的线程中运行。
    def run(self):
        # 声明全局变量，互斥锁
        global lock

        # 初始化计数变量
        data_count = 0
        # 初始化传感器
        self.InitSensor()
        # 开启传感器
        self.StartSensor()

        while True:
            # 生成数据
            data_count  = data_count + 1
            # 原始信号
            signal      = math.sin(data_count) * 10
            # 模拟噪声
            noise       = random.uniform(0, 5)
            # 最终数据
            data        = int(signal + noise)

            # 获取互斥锁
            lock.acquire()

            # 接收命令
            cmd = self.RecvMasterCMD()

            # 根据命令进行相关操作
            if cmd == SensorClass.STOP_CMD:
                # 如果接收到停止命令，停止传感器
                self.StopSensor()
                # 输出提示信息
                print("Sensor stop work !!!")
                return
            elif cmd == SensorClass.SENDID_CMD:
                # 如果接收到发送ID命令，发送传感器ID号
                self.SendSensorID()
            elif cmd == SensorClass.SENDVALUE_CMD:
                # 如果接收到发送数据命令，发送数据
                self.SendSensorValue(data)
            elif cmd == SensorClass.NONE_CMD:
                # 如果没有接收到指令
                print("Not Recv cmd!!!")

            # 释放互斥锁
            lock.release()
            # 延时0.5s
            time.sleep(0.5)

# 表示传感器数据过高的异常
class InvalidSensorValueError(Exception):
    def __init__(self,recvvalue,setvalue):
        super().__init__("Receive Sensor Value is too high")
        self.recvvalue = recvvalue
        self.setvalue = setvalue
    # 计算接收数据和设定数据的误差值
    def cal_offset(self):
        offset = self.setvalue - self.recvvalue
        return offset

# 定义了命令的枚举类
class CMD(Enum):
    START_CMD       =   0
    STOP_CMD        =   1
    SENDID_CMD      =   2
    SENDVALUE_CMD   =   3

class MasterClass(SerialClass,PlotClass):
    '''
    MasterClass：该类表示主机类，主要用于接收传感器数据、收发指令等

    具有如下属性：
        state       —— 表示主机工作状态
        port        —— 表示主机端口号
        wintitle    —— 表示窗口标题
        ... ...

    具有如下方法：
        StartMaster     —— 开启主机
        StopMaster      —— 停止主机
        RecvSensorValue —— 接收传感器数据值
        ... ...
    '''
    # 类变量：
    #   BUSY_STATE  -忙碌状态-0
    #   IDLE_STATE  -空闲状态-1
    BUSY_STATE, IDLE_STATE = (0, 1)
    # 类变量：
    #   START_CMD       - 开启命令      -0
    #   STOP_CMD        - 关闭命令      -1
    #   SENDID_CMD      - 发送ID命令    -2
    #   SENDVALUE_CMD   - 发送数据命令   -3
    START_CMD, STOP_CMD, SENDID_CMD, SENDVALUE_CMD = (0, 1, 2, 3)

    # 类的初始化
    def __init__(self,state:int = IDLE_STATE,port:str = "COM17",wintitle:str="Basic plotting examples",plottitle:str="Updating plot",width:int=1000,height:int=600):

        # 分别调用不同父类的__init__方法
        SerialClass.__init__(self,port)
        PlotClass.__init__(self,wintitle,plottitle,width,height)
        self.valuequeue   = queue.Queue(10)
        self.__masterstatue = state
        # 初始化完成的标志量
        self.INIT_FLAG = False
        # 文件保存路径
        self.savepath = "G:\\Python面向对象编程\\Demo\\file.csv"
        # 创建FileIOClass类的实例化对象
        self.fileio = FileIOClass(self.savepath)
        print("MASTER INIT SUCCESSS")
        logging.info("MASTER INIT SUCCESSS")

    @classmethod
    def MasterInfo(cls):
        print("Info : "+str(cls))

    # 开启主机
    def StartMaster(self):
        '''
            StartMaster方法——开启主机
            调用SerialClass.OpenSerial()方法
        :return: 无返回值
        '''
        super().OpenSerial()
        print("START MASTER :"+self.dev.port)
        logging.info("START MASTER :"+self.dev.port)

    # 停止主机
    def StopMaster(self):
        super().CloseSerial()
        print("CLOSE MASTER :" + self.dev.port)
        logging.info("CLOSE MASTER :" + self.dev.port)

    # 接收传感器ID号
    def RecvSensorID(self):
        sensorid = super().ReadSerial()
        print("MASTER RECIEVE ID : " + str(sensorid))
        logging.info("MASTER RECIEVE ID : " + str(sensorid))
        return sensorid

    # 接收传感器数据
    def RecvSensorValue(self):
        try:
            # 设定的阈值
            setvalue = 99
            data = super().ReadSerial()

            # 如果接收的传感器数据大于阈值
            if data >= setvalue:
                raise InvalidSensorValueError(data,setvalue)

            print("MASTER RECIEVE DATA : " + str(data))
            logging.info("MASTER RECIEVE DATA : " + str(data))
            self.valuequeue.put(data)
        except InvalidSensorValueError as e:
            print("invalid sensor value",e.args)
            print("value offset is : ",e.cal_offset())
        return data

    # 主机发送命令
    def SendSensorCMD(self,cmd):
        super().WriteSerial(str(cmd))
        print("MASTER SEND CMD : " + str(cmd))
        logging.info("MASTER SEND CMD : " + str(cmd))

    # 主机返回工作状态-
    def RetMasterStatue(self):
        return self.__masterstatue

    # 重写父类的DataUpdate方法
    def DataUpdate(self):
        self.SendSensorCMD(self.SENDVALUE_CMD)
        self.value = self.RecvSensorValue()
        self.WriteSerial("Recv:"+str(self.value))
        self.GetValue(self.value)
        self.curve.setData(self.valuelist)
        print("PLOT UPDATA : " + str(self.value))
        logging.info("PLOT UPDATA : " + str(self.value))

if __name__ == "__main__":
    pass