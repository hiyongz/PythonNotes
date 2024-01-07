
import logging
import math
from random import randint


class GetData:
    def __init__(self):
        self.logger = logging.getLogger("fatherModule.son.module")

    def getFSPL(self):
        # 数据1：时间（s）- 距离(km)
        time_list = list(range(0, 500, 5))
        initial_value = 1000  # 初始值km
        length = 100  # 生成列表的长度
        distance_list = []
        # accumulated_list = [initial_value + randint(15 , 30) for i in range(length)]
        for i in range(length):
            initial_value = initial_value + randint(15 , 30)
            distance_list.append(initial_value)

        # 数据2：距离(km) — 自由空间传输损耗（dB）
        fspl_list = list(map(self.fspl, distance_list))
        return time_list, distance_list, fspl_list
    
    def fspl(self, distance):
        # 发射功率固定为28GHz
        # FSPL = 20×lg(df) + 32.44        
        return 20 * math.log10(distance * 28000) + 32.44