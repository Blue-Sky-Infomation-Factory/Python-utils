from abc import ABC
from math import log2
from multiprocessing.shared_memory import SharedMemory
from struct import calcsize, pack, pack_into, unpack, unpack_from
from typing import Iterator, List, Literal, Tuple
from array import array
from inspect import BufferFlags

from .abstractmeta import AbstractMeta, realabstractmethod

def format_info(format: str):
	byte_length = calcsize(format)
	return (format, int(log2(byte_length)), byte_length)

class TypedArrayMeta(ABC, AbstractMeta):
	@property
	@realabstractmethod
	def format(self) -> Tuple[str, int, int]: ...
class TypedArray(metaclass=TypedArrayMeta):
	def __init__(self, buffer: bytearray | bytes | int | List | Tuple | array | memoryview | SharedMemory) -> None:
		[format, offset, byte_length] = self.__class__.format
		if isinstance(buffer, (memoryview, SharedMemory)):
			if isinstance(buffer, SharedMemory): buffer = buffer.buf
			if buffer.nbytes % byte_length: raise ValueError(f"The length in bytes of buffer must be a multiple of {byte_length}.")
			self.__buffer = buffer
		elif isinstance(buffer, (bytearray, bytes)):
			if len(buffer) % byte_length: raise ValueError(f"The length in bytes of buffer must be a multiple of {byte_length}.")
			self.__buffer = memoryview(buffer)
		elif isinstance(buffer, array):
			if buffer.itemsize != byte_length: raise ValueError(f"The itemsize of array must be {byte_length}.")
			self.__buffer = memoryview(buffer)
		elif isinstance(buffer, int):
			self.__buffer = memoryview(bytearray(buffer << offset))
		elif isinstance(buffer, (list, tuple)):
			self.__buffer = memoryview(pack(f"{len(buffer)}{format}", *buffer))
		else: raise TypeError("Argument 'buffer' must be one of the following types: (bytearray | bytes | int | List | Tuple | array | memoryview | SharedMemory).")

	def __init_subclass__(cls):
		[format, offset, _] = cls.format
		cls.__getitem__ = lambda self, index: unpack_from(format, self.__buffer, index << offset)[0]
		cls.__setitem__ = lambda self, index, value: pack_into(format, self.__buffer, index << offset, value)

	@classmethod
	def from_iterator(cls, length: int, iterator: Iterator):
		[format, _, _] = cls.format
		if length < 0: raise ValueError("Argument 'length' must be non-negative.")
		if not isinstance(iterator, Iterator): raise TypeError("Argument 'iterator' must be an iterator.")
		return cls(pack(f"{length}{format}", *iterator))

	@property
	def is_readonly(self): return self.__buffer.readonly
	@property
	def byte_length(self): return self.__buffer.nbytes
	
	def __getitem__(self, index: int):
		[format, offset, _] = self.__class__.format
		return unpack_from(format, self.__buffer, index << offset)[0]
	def __setitem__(self, index: int, value: int | float):
		[format, offset, _] = self.__class__.format
		pack_into(format, self.__buffer, index << offset, value)
	def __iter__(self):
		for i in range(len(self)): yield self[i]
	def __len__(self): return self.__buffer.nbytes >> self.__class__.format[1]
	def to_tuple(self):
		buffer = self.__buffer
		[format, offset, _] = self.__class__.format
		return unpack(f"{buffer.nbytes >> offset}{format}", buffer)
	def __repr__(self):
		length = len(self)
		temp = []
		if length > 10:
			for i in range(10): temp.append(str(self[i]))
			temp.append("...")
		else:
			for i in range(length): temp.append(str(self[i]))
		return f"{self.__class__.__name__}({length})[{', '.join(temp)}]"
	def __buffer__(self, flags: int):
		if BufferFlags.WRITABLE & flags and self.__buffer.readonly: raise BufferError("Internal buffer is not writable.")
		return self.__buffer

format_codes = { "i8": "b", "i16": "h", "i32": "i", "i64": "q", "f16": "e", "f32": "f", "f64": "d" }
def gen_array_type(is_float_type: bool, is_signed: bool, endian: Literal[0,1,2], byte_length: int):
	bit_length = byte_length << 3
	format_code = format_codes[f"{"f" if is_float_type else "i"}{bit_length}"]
	if not is_signed and not is_float_type: format_code = format_code.upper()
	class_name = f"{"" if is_signed else "u"}{"float" if is_float_type else "int"}{bit_length}{("LE" if endian == 1 else "BE") if endian else ""}Array"
	class_name = class_name[0].upper() + class_name[1:]
	if endian and byte_length != 1:
		format_code = ("<" if endian == 1 else ">") + format_code
	class meta(TypedArrayMeta):
		__format = format_info(format_code)
		@property
		def format(self): return self.__format
	class array_type(TypedArray, metaclass=meta): pass
	array_type.__name__ = array_type.__qualname__ = class_name
	return array_type

global_this = globals()
formats = [
	(False, True, 0, 1),
	(False, False, 0, 1),
	(False, False, 0, 2),
	(False, False, 1, 2),
	(False, False, 2, 2),
	(False, True, 0, 2),
	(False, True, 1, 2),
	(False, True, 2, 2),
	(False, False, 0, 4),
	(False, False, 1, 4),
	(False, False, 2, 4),
	(False, True, 0, 4),
	(False, True, 1, 4),
	(False, True, 2, 4),
	(False, False, 0, 8),
	(False, False, 1, 8),
	(False, False, 2, 8),
	(False, True, 0, 8),
	(False, True, 1, 8),
	(False, True, 2, 8),
	(True, True, 0, 4),
	(True, True, 1, 4),
	(True, True, 2, 4),
	(True, True, 0, 8),
	(True, True, 1, 8),
	(True, True, 2, 8)
]
for item in formats:
	array_type = gen_array_type(*item) # type: ignore
	global_this[array_type.__name__] = array_type

del global_this, formats, array_type