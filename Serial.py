# Python env   : Python 3.12 (parallel) (2)
# G:\miniconda\setup\envs\parallelpython.exe
# -*- coding: utf-8 -*-
# @Time    : 2024/2/16 11:03
# @Author  : 李清水
# @File    : Serial.py
# @Description : 定义了SerialClass的属性和方法

# 串口相关库
import serial
import serial.tools.list_ports
# 日志输出相关库
import logging

# 在配置下日志输出目标文件和日志格式
LOG_FORMAT="%(asctime)s-%(levelname)s-%(message)s"
logging.basicConfig(filename='my.log',level=logging.DEBUG,format=LOG_FORMAT)

class SerialClass:
    # 限定SerialClass对象只能绑定以下属性
    __slots__ = ('dev','_SerialClass__devstate')
    # 初始化
    # 使用默认参数
    def __init__(self,
                 devport:str     = "COM17",
                 devbaudrate:int = 115200,
                 devbytesize:int = serial.EIGHTBITS,
                 devparity  :str = serial.PARITY_NONE,
                 devstopbits:int = serial.STOPBITS_ONE):
        # 直接传入serial.Serial()类
        self.dev             = serial.Serial()
        self.dev.port        = devport
        self.dev.baudrate    = devbaudrate
        self.dev.bytesize    = devbytesize
        self.dev.parity      = devparity
        self.dev.stopbits    = devstopbits
        # 表示串口设备的状态-打开或者关闭
        # 初始化时为关闭
        self.__devstate      = False

        print("SerialClass init")
        logging.info("SerialClass init")

    # 取值方法
    @property
    def devstate(self):
        return self.__devstate

    # 打开串口
    def OpenSerial(self):
        print("SerialClass-OpenSerial")
        logging.info("SerialClass-OpenSerial")
        self.dev.open()
        self.__devstate = True

    # 关闭串口
    def CloseSerial(self):
        print("SerialClass-CloseSerial")
        logging.info("SerialClass-CloseSerial")
        self.dev.close()
        self.__devstate = False

    # 串口读取
    def ReadSerial(self):
        print("SerialClass-ReadSerial")
        logging.info("SerialClass-ReadSerial")
        if self.__devstate:
            # 阻塞方式读取
            # 按行读取
            data = self.dev.readline()
            # 收到为二进制数据
            # 用utf-8编码将二进制数据解码为unicode字符串
            # 字符串转为int类型
            data = int(data.decode('utf-8', 'replace'))
            return data

    # 串口写入
    def WriteSerial(self,write_data):
        print("SerialClass-WriteSerial")
        logging.info("SerialClass-WriteSerial")
        if self.__devstate:
            # 非阻塞方式写入
            self.dev.write(write_data.encode())
            # 输出换行符
            # write的输入参数必须是bytes 格式
            # 字符串数据需要encode()函数将其编码为二进制数据，然后才可以顺利发送
            # \r\n表示换行回车
            self.dev.write('\r\n'.encode())

    def RetSerialState(self):
        if self.dev.isOpen():
            self.__devstate = True
            return True
        else:
            self.__devstate = False
            return False

class DevClass(SerialClass):
    def __init__(self,port:str = "COM1"):
        super().__init__(port)

    # 开启设备
    def StartDev(self):
        super().OpenSerial()
        print("START Dev :" + self.dev.port)

    def ReadSerial(self,byte_size):
        if super().RetSerialState():
            data = self.dev.read(byte_size)
            data = int(data.decode('utf-8', 'replace'))
            return data

# 判断串口类对象的串口是否开启
def IsSerialConnected(serialclass):
    return serialclass.RetSerialState()