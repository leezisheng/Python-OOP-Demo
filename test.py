from collections import namedtuple
from enum import Enum
from enum import unique
# 使用typing模块提供的复合注解功能
import datetime
import time

# 定义定时器事件类
class TimedEvent:
    def __init__(self, endtime, callback):
        '''
        初始化方法，存储endtime和callback
        :param endtime:  callback执行前需要等待的时间
        :param callback: 回调函数，即到达执行时间后调用的函数
        '''
        self.endtime = endtime
        self.callback = callback
    def ready(self):
        '''
        判断是否事件已经到达了该执行的适合
        :return:
        '''
        return self.endtime <= datetime.datetime.now()

# 定义定时器类，轮询检测实现任务调度
class Timer:
    def __init__(self):
        '''
        初始化方法，定义一个events列表存储事件
        '''
        self.events = []
    def call_after(self, delay, callback):
        '''
        添加新的事件
        :param delay: 执行回调方法之前要等待的秒数
        :param callback: 回调方法
                         callback函数应该接收一个参数：执行调用的计时器
        :return:
        '''
        end_time = (datetime.datetime.now() +
                    datetime.timedelta(seconds=delay))
        self.events.append(TimedEvent(end_time, callback))
    def run(self):
        '''
        轮询检测，执行到达执行时间的回调函数
        :return: None
        '''
        # 轮询检测，执行到达执行时间的回调函数
        while True:
            # 使用一个生成器表达式，将将时间已到的事件过滤出来
            ready_events = (e for e in self.events if e.ready())
            # 按照顺序执行
            for event in ready_events:
                event.callback(self)
                # 执行完成后，移除已执行完毕的任务
                self.events.remove(event)
            # 在每次迭代过程中休眠 0.5 秒以防止系统死机
            time.sleep(0.5)

def format_time(message, *args):
    '''
    用字符串的 format 方法将当前时间添加到信息中，并说明变量参数
    :param message: 接收任意数量的定位参数
    :param args:    用于在函数中处理传递的位置参数序列
    :return: None
    '''
    # 当前的时间，格式为：时-分-秒
    now = datetime.datetime.now().strftime("%I:%M:%S")
    # 格式化打印参数
    print(message.format(*args, now=now))

# 回调函数：任务一
def Task_One(timer):
    format_time("{now}: Called Task One")

# 回调函数：任务二
def Task_Two(timer):
    format_time("{now}: Called Task Two")

# 回调函数：任务三
def Task_Three(timer):
    format_time("{now}: Called Task Three")

# 定义类
class Repeater:
    def __init__(self):
        '''

        '''
        self.count = 0
    def repeater(self, timer):
        '''
        在函数中在创建一个定时任务
        :param timer: 定时器
        :return: None
        '''
        format_time("{now}: repeat {0}", self.count)
        self.count += 1
        # 类的方法也可以用作回调函数
        timer.call_after(5, self.repeater)

# # 创建定时器对象
# timer = Timer()
# repeater = Repeater()
# # 添加回调函数，类的方法
# timer.call_after(5, repeater.repeater)
# # 开始运行定时器
# format_time("{now}: Starting")
# timer.run()

# 导入协议Protocol
from typing import Protocol
import typing
# 定义Printable协议，需要具有打印方法
@typing.runtime_checkable
class Printable(Protocol):
    def print(self) -> None:
        pass
# 定义Book类，具有打印方法
class Book:
    def __init__(self, title: str):
        self.title = title

    def print(self) -> None:
        print(f"Book Title: {self.title}")
# 声明任何传入print_object的对象必须满足Printable协议
def print_object(obj: Printable) -> None:
    obj.print()
# 定义CD类，没有打印方法
class CD:
    def __init__(self, title: str):
        self.title = title

    def play(self) -> None:
        print(f"play music Title: {self.title}")

# book_obj = Book("Piece and Love")
# print_object(book_obj)
# cd_obj = CD("Piece and Love")
# print(isinstance(Book,Printable))
# assert isinstance(book_obj,Printable)
# print(isinstance(CD,Printable))
# assert isinstance(cd_obj,Printable)

template = """
public class {0} {{
public static void main(String[] args) {{
System.out.println("{1}");
}}
}}"""
# print(template.format("MyClass", "print('hello world')"));

# import sys
# import re
# pattern = sys.argv[1]
# search_string = sys.argv[2]
# match = re.match(pattern, search_string)
#
# if match:
#     template = "'{}' matches pattern '{}'"
# else:
#     template = "'{}' does not match pattern '{}'"
# print(template.format(search_string, pattern))

import json
class Contact:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    @property
    def full_name(self):
        return("{} {}".format(self.first, self.last))

c = Contact("John", "Smith")
# print(json.dumps(c.__dict__))

template = """
public class {0} {{
    public static void main(String[] args) {{
        System.out.println("{1}");
    }}
}}"""
# print(template.format("MyClass", "print('hello world')"));

emails = ("a@example.com", "b@example.com")
message = {
            'subject': "You Have Mail!",'message': "Here's some mail for you!"
          }
template = """ 
From: <{0[0]}> 
To: <{0[1]}> 
Subject: {message[subject]} 
{message[message]}"""
# print(template.format(emails, message=message))
# print(message['subject'])

emails = ("a@example.com", "b@example.com")
message = {
            'emails': emails,
            'subject': "You Have Mail!",
            'message': "Here's some mail for you!"
          }
template = """ 
From: <{0[emails][0]}> 
To: <{0[emails][1]}> 
Subject: {0[subject]} 
{0[message]}"""
# print(template.format(message))

from datetime import datetime

now = datetime.now()
# 格式化日期和时间
formatted_date = "Current date and time: {:%Y-%m-%d %H:%M:%S}".format(now)
# print(formatted_date)

import sys
# print(sys.getdefaultencoding())

# import re
# # 由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了
# print(re.match(r'^(\d+)(0*)$', '102300').groups())
# # 加个?就可以让\d+采用非贪婪匹配：
# print(re.match(r'^(\d+?)(0*)$', '102300').groups())

# import pickle
#
# # 待序列化的列表对象
# some_data = ["a list", "containing", 5, "values including another list", ["inner", "list"]]
#
# # 序列化对象，将列表存储到文件中
# # 使用 open() 函数打开一个名为 "pickled_list" 的文件
# # 以二进制写入模式 'wb' 打开文件
# with open("pickled_list", 'wb') as file:
#     # 使用 pickle.dump() 方法将 some_data 对象序列化并写入到文件中
#     pickle.dump(some_data, file)
#
# # 反序列化对象，将文件中列表载入
# # 开同一个文件，以二进制读取模式 'rb' 打开文件
# with open("pickled_list", 'rb') as file:
#     # 使用 pickle.load() 方法从文件中反序列化出 some_data 对象
#     loaded_data = pickle.load(file)
#
# loaded_data.append("1")
# # 打印载入后的列表
# print(loaded_data)
# # 判断列表文件是否相同
# assert loaded_data == some_data



import shelve

# 使用shelve.open()函数创建或打开一个Shelve文件
with shelve.open('mydata.db') as shelf:
    # 使用 shelf['key'] = value 的方式将键值对写入到 Shelve 文件中
    shelf['name'] = 'Alice'
    shelf['age'] = 30
    shelf['scores'] = [95, 88, 72]

    # 使用 shelf['key'] 的方式从 Shelve 文件中读取数据
    # 将其赋值给相应的变量
    name = shelf['name']
    age = shelf['age']
    scores = shelf['scores']

# print(f'Name: {name}')
# print(f'Age: {age}')
# print(f'Scores: {scores}')
#
# with shelve.open('mydata.db', writeback=True) as shelf:
#     # 更新数据
#     shelf['name'] = 'Bob'
#     # 删除数据
#     del shelf['age']
#     name = shelf['name']
#     print(name)
#     try:
#         age = shelf['age']
#         print(age)
#     except:
#         print("No ages")



import json

# # 人员信息列表
# humaninfodic={
#     'age'   : 18,
#     'name'  : True,
#     'gender': 10,
#     'email' : 11.1,
# }
#
#
# # 序列化到文件中
# with open('test.json', 'w') as fp:
#     json.dump(humaninfodic, fp, indent=4)
#
# # 反序列化文件中的内容
# with open('test.json', 'r') as fp:
#     dic = json.load(fp)
#     print(dic)


import json

# 定义联系人类
class Contact:
    def __init__(self, first, last):
        # 属性1，first name是名字
        self.first = first
        # 属性2，last name是姓氏
        self.last = last
    @property
    def full_name(self):
        return("{} {}".format(self.first, self.last))

# 自定义序列化编码器类
class ContactEncoder(json.JSONEncoder):
    # default 方法检查了我们想要序列化的对象类型
    def default(self, obj):
        # 如果是联系人类，我们手动将其转换为字典
        if isinstance(obj, Contact):
            return {
                    # 传递了一个额外的属性来说明这是一个联系人对象
                    # 因为没有其他办法可以在载入之后知道它的类型
                    'is_contact': True,
                    'first': obj.first,
                    'last': obj.last,
                    'full': obj.full_name}
        # 否则，让其父类来处理序列化（假设它是基本类型，json 知道如何处理）
        return super().default(obj)

# 定义一个JSON文件解码器函数
def decode_contact(dic):
    # 写一个函数接受字典为参数
    # 检查是否包含 is_contact 变量来决定是否将其转换为联系人
    if dic.get('is_contact'):
        return Contact(dic['first'], dic['last'])
    else:
        return dic

# if __name__ == '__main__':
#     c = Contact("John", "Smith")
#     data = json.dumps(c, cls=ContactEncoder)
#     print(data)
#     c = json.loads(data, object_hook=decode_contact)
#     print(c.full_name)

from collections import defaultdict

class StatsList(list):
    def mean(self):
        return sum(self) / len(self)
    def median(self):
        if len(self) % 2:
            return self[int(len(self) / 2)]
        else:
            idx = int(len(self) / 2)
            return (self[idx] + self[idx-1]) / 2
    def mode(self):
        freqs = defaultdict(int)
        for item in self:
            freqs[item] += 1
        mode_freq = max(freqs.values())
        modes = []
        for item, value in freqs.items():
            if value == mode_freq:
                modes.append(item)
            return modes


import threading
import time


def thread1():
    while True:
        time.sleep(1)
        print(time.strftime('%H:%M:%S'), 'hahaha')


def thread2():
    while True:
        time.sleep(2)
        print(time.strftime('%H:%M:%S'), 'lalala')


thread_thred1 = threading.Thread(target=thread1)
thread_thred1.start()
thread_thread2 = threading.Thread(target=thread2)
thread_thread2.start()