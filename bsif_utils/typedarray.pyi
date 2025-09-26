from abc import ABC
from multiprocessing.shared_memory import SharedMemory
from typing import Any, Iterator, List, Literal, Tuple, Type, Union
from array import array

from .abstractmeta import AbstractMeta

def format_info(format_code: str) -> Tuple[str, int, int]:
	"""Get meta class format info by struct format code.
	
	Example: int32, little endian = "<i\""""

class TypedArrayMeta(ABC, AbstractMeta):
	@property
	def format(self) -> Tuple[str, int, int]:
		"""[0]: struct format code ; [1]: offset of item index to address ; [2]: item size in bytes"""

class TypedArray(ABC, metaclass=TypedArrayMeta):
	"""Base class.
	
	This class implemented all methods already without the format in meta.
	
	If you want to create a type by yourself, all you need to do is implement a TypedArrayMeta with format and create a class like `class Formatted(TypedArray, metaclass=meta)`."""
	def __init__(
		self,
		buffer: (
			bytearray
			| bytes
			| int
			| List[int]
			| List[float]
			| Tuple[int]
			| Tuple[float]
			| array
			| memoryview
			| SharedMemory
		),
	) -> None: ...
	@classmethod
	def from_iterator(cls, length: int, iterator: Iterator[Any]) -> TypedArray: ...
	@property
	def is_readonly(self) -> bool: ...
	@property
	def byte_length(self) -> int: ...
	def __getitem__(self, index: int) -> Union[int, float]: ...
	def __setitem__(self, index: int, value: Union[int, float]) -> None: ...
	def __iter__(self) -> Iterator[Union[int, float]]: ...
	def __len__(self) -> int: ...
	def to_tuple(self) -> Tuple[Union[int, float], ...]: ...
	def __repr__(self) -> str: ...
	def __buffer__(self, flags: int) -> memoryview: ...
	
def gen_array_type(is_float_type: bool, is_signed: bool, endianness: Literal[0,1,2], byte_length: Literal[1,2,4,8]) -> Type[TypedArray]:
	"""Generate a TypedArray type.
	
	endianness: Specified buffer endianness. 0: native, 1: liitle endian, 2: big endian
	
	byte_length: Specified buffer item size in bytes."""

class Uint8Array(TypedArray): ...
class Int8Array(TypedArray): ...
class Uint16Array(TypedArray): ...
class Int16Array(TypedArray): ...
class Uint32Array(TypedArray): ...
class Int32Array(TypedArray): ...
class Uint64Array(TypedArray): ...
class Int64Array(TypedArray): ...
class Float32Array(TypedArray): ...
class Float64Array(TypedArray): ...

__all__ = [
	"TypedArrayMeta",
	"TypedArray",
	"format_info",
	"gen_array_type",
	"Int8Array",
	"Uint8Array",
	"Uint16Array",
	"Int16Array",
	"Uint32Array",
	"Int32Array",
	"Uint64Array",
	"Int64Array",
	"Float32Array",
	"Float64Array",
]