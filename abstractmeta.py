from abc import ABCMeta, abstractmethod
from typing import Callable

def _abstract_method(*_): raise TypeError("Not implemented")
def realabstractmethod(_: Callable): return abstractmethod(_abstract_method)

class AbstractMeta(ABCMeta):
	def __call__(cls, *args, **kwds):
		meta = cls.__class__
		if len(meta.__abstractmethods__): raise TypeError(f"Can't instantiate class {cls.__name__} without an implementation for it's metaclass {meta.__name__}")
		return super().__call__(*args, **kwds)