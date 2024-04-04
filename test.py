from collections import namedtuple

_Sensor = namedtuple("Sensor","ID CURRENTVALUE MAXVALUE MINVALUE")

class Sensor(_Sensor):
    '''
        这是一个继承自表示传感器数据的命名元组的类
        具有四个属性：
            （1） ID              ： 表示传感器ID号
            （2） CURRENTVALUE    ： 传感器采集到的当前数据值
            （3） MAXVALUE        ： 传感器采集到的最大数据值
            （4） MINVALUE        ： 传感器采集到的最小数据值
    '''
sensor_tuple=Sensor(ID="16",CURRENTVALUE=32,MAXVALUE=62,MINVALUE=2)
print(sensor_tuple.__doc__)
