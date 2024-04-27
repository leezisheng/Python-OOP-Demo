# Python env   : Python 3.12 (parallel) (2)
# G:\miniconda\setup\envs\parallelpython.exe
# -*- coding: utf-8 -*-
# @Time    : 2024/2/16 11:10
# @Author  : 李清水
# @File    : FileIO.py
# @Description : 定义了FileIOClass的属性和方法

# 日志输出相关库
import logging
# 文件读写相关库
import csv
# 使用typing模块提供的复合注解功能
from typing import List

# 日志设置
LOG_FORMAT="%(asctime)s-%(levelname)s-%(message)s"
logging.basicConfig(filename='my.log',level=logging.DEBUG,format=LOG_FORMAT)

class FileIOClass:
    def __init__(self,path:str="G:\\Python面向对象编程\\Demo\\file.csv"):
        '''
        初始化csv文件和列标题
        :param path: 文件路径和文件名
        '''
        self.path   = path
        try:
            # path为输出路径和文件名，newline=''是为了不出现空行
            self.csvFile = open(path, "w+", newline='')
            # rowname为列名，index-索引，data-数据
            self.rowname = ['index', 'data']
            # 返回一个writer对象，将用户的数据在给定的文件型对象上转换为带分隔符的字符串
            self.writer = csv.writer(self.csvFile)
            # 写入csv文件的列标题
            self.writer.writerow(self.rowname)
        except (FileNotFoundError, IOError) as e:
            print("Could not open file",e.__class__.__name__)
            print("The exception arguments were", e.args)
            logging.info("Could not open file")
        except KeyboardInterrupt:
            print("Cancell the file operation")
            logging.info("Cancell the file operation")
        finally:
                self.CloseFile()

    def WriteFile(self,index:List[int],data:List[int])->None:
        '''
        :param index: 传感器索引列表
        :param data:  传感器数据列表
        :return:
        '''
        writedatalist = []
        try:
            for i in range(len(data)):
                writedatalist.append([index[i],data[i]])
                # 将列表中的每个元素将被写入CSV文件的一列中
                self.writer.writerow(writedatalist[i])
        except (FileNotFoundError, IOError):
            print("Could not open file")
            logging.info("Could not open file")
        except KeyboardInterrupt:
            print("Cancell the file operation")
            logging.info("Cancell the file operation")
        finally:
                self.CloseFile()

    def CloseFile(self)->None:
        '''
        关闭文件
        :return: None
        '''
        self.csvFile.close()

