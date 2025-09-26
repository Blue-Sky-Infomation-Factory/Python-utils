from typing import List

class PiecewiseRange:
	def __init__(self):
		self.__indexes: List[List[int]] = []

	def __iter__(self):
		for range_item in [range(item[0], item[1] + 1) for item in self.__indexes]: yield from range_item

	def add_range(self, min_value: int, max_value: int):
		if max_value < min_value: raise ValueError("Max less than min.")
		indexes = self.__indexes
		length = len(indexes)
		if not length:
			indexes.append([min_value, max_value])
			return
		
		first_item = indexes[0]
		range_min = first_item[0]
		if max_value <= range_min:
			if max_value >= range_min - 1: first_item[0] = min_value
			else: indexes.insert(0, [min_value, max_value])
			return
		max_index = length - 1
		last_item = indexes[max_index]
		range_max = last_item[1]
		if min_value >= range_max:
			if min_value <= range_max + 1: last_item[1] = max_value
			else: indexes.append([min_value, max_value])
			return
		
		start_index = 0
		end_index = max_index
		for index in range(length):
			item = indexes[index]
			if min_value < item[0]:
				if not index: break
				last_index = index - 1
				start_index = last_index if indexes[last_index][1] + 1 == min_value else index
				break
			if min_value <= item[1]:
				start_index = index
				break
		for index in range(start_index, length):
			item = indexes[index]
			if max_value < item[0]:
				end_index = index if max_value == item[0] - 1 else index - 1
				break
			if max_value <= item[1]:
				end_index = index
				break

		if end_index < start_index:
			indexes.insert(start_index, [min_value, max_value])
			return
		area_min = min(indexes[start_index][0], min_value)
		area_max = max(indexes[end_index][1], max_value)
		for index in range(start_index, end_index + 1): indexes.pop(start_index)
		indexes.insert(start_index, [area_min, area_max])