# -*-coding:utf-8-*-
import itertools
from functools import reduce


class mac_generate():
    def __init__(self):
        self.macs = None

    def mac_permute(self, mac, mac_start):
        """MAC地址后6位组合生成

        每一位的地址顺序为0-f

        :param mac: 格式：00:2X:XX，X表示0-f所有组合

        :param mac_start: 开始MAC, 格式：08:XX:XX, 表示前两位从08开始

        :return: 生成的MAC地址组合列表

        Example:
        | mac_permute | 00:2X:XX | XX:XX:XX |

        m = mac_generate()
        m.mac_permute("00:2X:XX","XX:XX:XX")
        """

        # 分割输入MAC地址
        mac_seg = mac.split(":")
        mac_segs = reduce(lambda x, y: x + y, mac_seg)
        mac_segs = list(mac_segs)

        mac_start_seg = mac_start.split(":")
        mac_start_segs = reduce(lambda x, y: x + y, mac_start_seg)
        mac_start_segs = list(mac_start_segs)

        # 计算MAC组合
        for index, mac in enumerate(mac_segs):
            if mac == "X":
                # 枚举
                self.macs = self._macs()
                if mac_start_segs[index] != "X":
                    start_index = self.macs.index(mac_start_segs[index])
                    mac_segs[index] = self.macs[start_index:]
                else:
                    mac_segs[index] = self.macs

        # 将每一位放入列表中
        for i in range(len(mac_segs)):
            if isinstance(mac_segs[i], str):
                mac_segs[i] = [mac_segs[i]]

        # 生成所有组合（笛卡尔积）
        mac_list = list(itertools.product(mac_segs[0], mac_segs[1], mac_segs[2], mac_segs[3], mac_segs[4], mac_segs[5]))
        macs = list(map(lambda x: x[0] + x[1] + ":" + x[2] + x[3] + ":" + x[4] + x[5], mac_list))
        # print(macs)
        return macs

    def _macs(self):
        if self.macs is None:
            macs = [str(i) for i in range(10)]
            macs = macs + ["a", "b", "c", "d", "e", "f"]
            return macs
        return self.macs
