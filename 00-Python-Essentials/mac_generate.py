# -*-coding:utf-8-*-
import itertools

class mac_generate():
	def __init__(self):
		self.macs = None

	def mac_permute(self, mac, mac_start):
		mac_seg = mac.split(":")
		mac_start_seg = mac_start.split(":")
		# print(mac_seg)
		for index, mac in enumerate(mac_seg):
			if mac == "XX":
				# 枚举
				self.macs = self._mac_permut()
				if mac_start_seg[index] != "XX":
					start_index = self.macs.index(mac_start_seg[index])
					mac_seg[index] = self.macs[start_index:]
				else:
					mac_seg[index] = self.macs

		for i in range(3):
			if isinstance(mac_seg[i], str):
				mac_seg[i] = [mac_seg[i]]

		mac_list = list(itertools.product(mac_seg[0], mac_seg[1], mac_seg[2]))
		macs = list(map(lambda x: x[0] + ":" + x[1] + ":" + x[2], mac_list))
		# print(macs)
		return macs

	def _mac_permut(self, flag=None):
		if self.macs is None:
			macs = [str(i) for i in range(10)]
			macs = macs + ["a", "b", "c", "d", "e", "f"]
			# 枚举
			# mac1 = list(zip(macs, macs))
			# mac2 = list(itertools.permutations(macs, 2))
			# mac = mac1 + mac2
			mac = list(itertools.product(macs, repeat=2))  # 笛卡尔积
			list_macs = list(map(lambda x: x[0] + x[1], mac))
			# print(len(list_macs))
			return list_macs
		return self.macs

	def test_permut_combi(self):
		# 排列
		l = [1, 2, 3]
		l1 = [11, 12, 13]
		l2 = [21, 22, 23]

		print(list(itertools.permutations(l, 2)))
		print(list(itertools.permutations(l, 3)))

		# 组合
		print(list(itertools.combinations(l, 2)))

		# 笛卡尔积
		print(list(itertools.product(l, l)))
		print(list(itertools.product(l, repeat=2)))
		print(list(itertools.product(l1, l2)))

m = mac_generate()
m.test_permut_combi()
m.mac_permute("00:XX:01","XX:XX:XX")

