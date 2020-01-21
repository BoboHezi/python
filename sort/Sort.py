#!/usr/bin/python

class Sort(object):
	"Sort class"

	def abacus_sort(self, origin):
		# 偏移值，处理小数情况
		# offset = 0
		# if min(origin) < 0:
		# 	offset = -min(origin)
		# 	origin = self.offset_everyone(origin, offset)

		# 获取行数，原始列表长度
		row = len(origin)
		# 获取列数，原始列表最大值
		cub = max(origin)

		# 创建原始二维数组
		origin_list = []
		i = 0
		for number in origin:
			list = []
			index = 0
			while index < cub:
				if index < abs(number):
					if number < 0:
						list.append(-1)
					else:
						list.append(1)
				else:
					list.append(0)
				index += 1
			origin_list.append(list)
			i += 1
		# self.print_two_dimension('origin two_dimension:\n', origin_list)
		sorted_list = self.overturn(self.sink(self.overturn(origin_list)))
		# self.print_two_dimension('sorted two_dimension:\n', sorted_list)

		sorted = [self.count_list(sorted_list[x]) for x in range(0, row)]
		# 回退偏移值
		# if offset != 0:
		# 	self.offset_everyone(sorted, -offset)
		return sorted

	# 数组值相加
	def count_list(self, list):
		number = 0
		for i in list:
			number += i
		return number

	# 矩阵翻转
	def overturn(self, source):
		row = len(source)
		cub = len(source[0])
		value = [[0 for c in range(row)] for r in range(cub)]
		i = 0
		for list in source:
			j = 0
			for number in list:
				(value[j])[i] = number
				j += 1
			i += 1
		return value

	# 数组每个值设置偏移
	def offset_everyone(self, list, offset):
		index = 0
		for number in list:
			number += offset
			list[index] = number
			index += 1
		return list

	# 下沉数据
	def sink(self, source):
		for list in source:
			list.sort()
		return source

	def print_two_dimension(self, tag, list):
		str_ = tag
		for row in list:
			str_ += '\t'
			for i in row:
				if i >= 0:
					str_ += ' '
				str_ += str(i)
				str_ += ' '
			str_ += '\n'
		print(str_)
