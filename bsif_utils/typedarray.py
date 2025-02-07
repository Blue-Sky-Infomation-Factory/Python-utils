from abc import ABC
from math import sqrt
from struct import calcsize, pack, pack_into, unpack, unpack_from
from typing import Iterator, List, Tuple

from abstractmeta import AbstractMeta, realabstractmethod

def format_info(format: str):
	byte_length = calcsize(format)
	return (format, int(sqrt(byte_length)), byte_length)

class TypedArrayMeta(ABC, AbstractMeta):
	@property
	@realabstractmethod
	def format(self) -> Tuple[str, int, int]: ...
class TypedArray(metaclass=TypedArrayMeta):
	def __init__(self, array: bytearray | bytes | int | List | Tuple) -> None:
		[format, offset, byte_length] = self.__class__.format
		if isinstance(array, (bytearray, bytes)):
			if len(array) % byte_length: raise ValueError(f"Length of array must be a multiple of {byte_length}.")
			self.__bytes = array
		elif isinstance(array, int):
			self.__bytes = bytearray(array << offset)
		elif isinstance(array, (list, tuple)):
			self.__bytes = pack(f"{len(array)}{format}", *array)
		else: raise TypeError("Argument 'array' must be one of the following types: (bytearray | bytes | int | List | Tuple).")
	
	def __init_subclass__(cls):
		[format, offset, _] = cls.format
		cls.__getitem__ = lambda self, index: unpack_from(format, self.__bytes, index << offset)[0]
		cls.__setitem__ = lambda self, index, value: pack_into(format, self.__bytes, index << offset, value)

	@classmethod
	def from_iterator(cls, length: int, iterator: Iterator):
		[format, _, _] = cls.format
		if length < 0: raise ValueError("Argument 'length' must be non-negative.")
		if not isinstance(iterator, Iterator): raise TypeError("Argument 'iterator' must be an iterator.")
		return Uint32Array(pack(f"{length}{format}", *iterator))

	@property
	def is_readonly(self): return isinstance(self.__bytes, bytes)
	@property
	def byte_length(self): return len(self.__bytes)
	
	def __getitem__(self, index: int):
		[format, offset, _] = self.__class__.format
		return unpack_from(format, self.__bytes, index << offset)[0]
	def __setitem__(self, index: int, value: int):
		[format, offset, _] = self.__class__.format
		pack_into(format, self.__bytes, index << offset, value)
	def __iter__(self):
		for i in range(len(self)): yield self[i]
	def __len__(self): return len(self.__bytes) >> self.__class__.format[1]
	def to_tuple(self):
		buffer = self.__bytes
		[format, offset, _] = self.__class__.format
		return unpack(f"{len(buffer) >> offset}{format}", buffer)
	def __repr__(self): return f"{self.__class__.__name__}({len(self)})[{','.join(hex(num) for num in self.to_tuple())}]"

class Uint32ArrayMeta(TypedArrayMeta):
	__format = format_info("I")
	@property
	def format(self): return self.__format
class Uint32Array(TypedArray, metaclass=Uint32ArrayMeta): pass

print(Uint32Array.format)